"""
Agent — agente conversazionale per Blender.

Trasforma richieste in linguaggio naturale in chiamate tool deterministiche,
con object resolution, conversation state, e debug visibile.
"""

import os, re, json, math, hashlib, traceback
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Any, Optional

from app.blender import (
    core_list_blend_files,
    core_render_preview,
    core_duplicate_version,
    get_versions_dir,
)
from app.blender_tools import (
    core_list_objects,
    core_inspect_object_detail,
    core_select_object,
    core_move_object,
    core_rotate_object,
    core_hide_object,
    core_show_object,
    core_duplicate_object,
    safe_operate,
)


# ─── Conversation State ────────────────────────────────


@dataclass
class ConversationState:
    conversation_id: str = ""
    history: list = field(default_factory=list)
    last_referenced_object: str | None = None
    last_created_object: str | None = None
    last_tool_call: str | None = None
    last_change_id: str | None = None
    current_blend: str = ""
    session_objects: dict = field(default_factory=dict)


# ─── Agent ─────────────────────────────────────────────


class Agent:
    """Agente conversazionale per comandi Blender."""

    # Pattern di intento con priorità (più alta = match prima)
    INTENTS = [
        (r"struttura|nella scena|cosa c[`']\u00e8|scene overview", 90, "inspect_scene"),
        (r"mostrami (tutti )?gli oggetti|lista oggetti|elenco", 80, "list_objects"),
        (r"come .* (costruit|fatt|componi|structur)", 70, "inspect"),
        (r"dettagli", 60, "inspect"),
        (r"analizza|ispeziona|esamina|descrivi", 60, "inspect"),
        (r"\bcreane|\bcrea (una )?copia( di)?|duplica|fai una copia|clona", 80, "duplicate"),
        (r"sposta|muovi|posiziona|trasla", 70, "move"),
        (r"ruota|gira|rotazion", 70, "rotate"),
        (r"nascondi|rendi invisibile", 60, "hide"),
        (r"mostra|rendi visibile|fai riapparire", 60, "show"),
        (r"seleziona", 50, "select"),
        (r"render|preview|anteprima|fammi vedere|mostra il risultat", 75, "render"),
        (r"annulla|revert|undo|torna indietro|non mi piace", 85, "undo"),
        (r"resetta|reset|ricomincia|nuova conversazione", 90, "reset"),
        (r"help|comandi|aiuto|cosa sai fare|menu|list.*command", 20, "help"),
    ]

    # Parole di connessione da ignorare nell'estrazione nome oggetto
    STOP_WORDS = {"di", "del", "della", "dello", "dei", "degli",
                  "un", "una", "uno", "il", "la", "lo", "le", "gli",
                  "al", "dal", "nel", "nella", "sul", "sulla",
                  "a", "da", "in", "con", "su", "per", "tra", "fra",
                  "che", "come", "dove", "quando", "verso"}

    def __init__(self):
        self.state = ConversationState()
        self.reset()

    # ── Public API ─────────────────────────────────────

    def reset(self):
        self.state = ConversationState(
            conversation_id=datetime.now(tz=timezone.utc).strftime("%Y%m%d-%H%M%S"),
            current_blend=self._find_default_blend(),
        )
        self.state.session_objects = {}

    def handle(self, message: str) -> dict:
        """Entrypoint: processa un messaggio utente e restituisce risposta."""
        msg = message.strip()
        self.state.history.append({"role": "user", "message": msg})

        debug = {"user_message": msg, "steps": []}

        try:
            # 2. Classifica intento
            intent, intent_conf = self._classify_intent(msg)
            debug["steps"].append({"step": "intent", "intent": intent, "confidence": intent_conf,
                                    "state": self._state_snapshot()})

            # 3. Estrai entità
            entities = self._extract_entities(msg, intent)
            debug["steps"].append({"step": "entities", "entities": entities})

            # 4. Risolvi riferimenti (pronomi, contesto)
            resolved = self._resolve_references(entities, intent)
            debug["steps"].append({"step": "resolution", "resolved": resolved})

            # 5. Esegui
            result = self._execute(intent, resolved)
            debug["steps"].append({"step": "execute", "result": {k: v for k, v in result.items()
                                      if k not in ("html",)}})

            # 6. Usa risposta dal risultato dell'esecuzione
            response = result.get("response", json.dumps(result))

            return {
                "status": result.get("status", "ok"),
                "response": response,
                "debug": debug,
                "state": self._state_snapshot(),
                **({k: v for k, v in result.items()
                    if k in ("version_id", "render_url", "new_object")}),
            }

        except Exception as e:
            debug["steps"].append({"step": "error", "error": str(e)[:500],
                                    "trace": traceback.format_exc()[:300]})
            return {
                "status": "error",
                "response": f"❌ {e}",
                "debug": debug,
                "state": self._state_snapshot(),
            }

    # ── Internals ─────────────────────────────────────

    def _find_default_blend(self) -> str:
        ws = os.environ.get("WORKSPACE_DIR", "/workspace")
        for c in ["base/PORTALE.blend", "base/PORTALE.blend1"]:
            if (Path(ws) / c).exists():
                return c
        for f in sorted(Path(ws).rglob("*.blend")):
            return str(f.relative_to(ws))
        return "base/PORTALE.blend"

    def _state_snapshot(self) -> dict:
        return {
            "last_referenced_object": self.state.last_referenced_object,
            "last_created_object": self.state.last_created_object,
            "last_tool_call": self.state.last_tool_call,
            "last_change_id": self.state.last_change_id,
            "current_blend": self.state.current_blend,
        }

    def _classify_intent(self, msg: str) -> tuple[str, float]:
        """Classifica l'intento del messaggio con confidence score."""
        msg_l = msg.lower().strip()
        for pattern, priority, intent in self.INTENTS:
            if re.search(pattern, msg_l):
                return intent, priority
        return "unknown", 0

    def _extract_entities(self, msg: str, intent: str) -> dict:
        """Estrae entità (nomi oggetti, offset, direzioni) dal messaggio."""
        msg_l = msg.lower().strip()
        entities = {}

        # Estrarre offset numerico (distanza/quantità)
        nums = re.findall(r"([-\d.]+)\s*(?:cm|m|°|gradi)?", msg_l)
        entities["numbers"] = [float(n) for n in nums if self._is_number(n)]

        # Estrarre direzioni
        dir_map = {
            "destra": "right", "sinistra": "left",
            "su": "up", "giù": "down", "giu": "down",
            "avanti": "forward", "indietro": "backward",
            "dietro": "backward", "sopra": "up", "sotto": "down",
            "right": "right", "left": "left", "up": "up", "down": "down",
            "lato": "right",
        }
        for word in msg_l.split():
            if word in dir_map:
                entities["direction"] = dir_map[word]
                break

        # Estrarre coordinate: "a X, Y, Z" oppure "(X, Y, Z)"
        coord_m = re.search(r"a\s*\(?([-\d.]+)\s*[,;]\s*([-\d.]+)\s*[,;]\s*([-\d.]+)", msg_l)
        if coord_m:
            entities["coordinates"] = (
                float(coord_m.group(1)),
                float(coord_m.group(2)),
                float(coord_m.group(3)),
            )

        # Estrarre angolo: "di N" dopo ruota
        if intent == "rotate":
            for n in entities.get("numbers", []):
                if n != 0:
                    entities["angle"] = n
                    break

        # Estrarre nome oggetto
        entities["object_name"] = self._extract_object_name(msg_l, intent)

        return entities

    def _is_number(self, s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False

    def _extract_object_name(self, msg_l: str, intent: str) -> str | None:
        """Estrae il nome dell'oggetto dal messaggio."""

        # Lista di parole che fermano la cattura del nome
        bound_words = {"e", "ed", "dimmi", "come", "dove", "quando",
                       "perché", "perche", "cosa", "quale", "quali",
                       "senza", "con", "che", "verso", "di", "a", "in",
                       "destra", "sinistra", "su", "giù", "giu",
                       "avanti", "indietro"}

        # Cerca dopo verbo + articolo/stopword
        verbs_patterns = [
            (r"\banalizza\s+(?:la\s+|l['\"]|un\s+|una\s+|uno\s+)?(.+)", "inspect"),
            (r"\bispeziona\s+(?:la\s+|l['\"]|un\s+|una\s+)?(.+)", "inspect"),
            (r"\b(?:crea|fai)\s+(?:una\s+)?copia\s+(?:di\s+)?(?:la\s+|l['\"]|un\s+|una\s+)?(.+)", "duplicate"),
            (r"\bduplica\s+(?:la\s+|l['\"]|un\s+|una\s+)?(.+)", "duplicate"),
            (r"\b(?:creane|fanne)\s+(?:una\s+)?copia(?:(?:\s+di)?.*)?$", "duplicate-nocap"),
            (r"\bsposta\s+(?:la\s+|l['\"]|un\s+|una\s+)?(.+)", "move"),
            (r"\bmuovi\s+(?:la\s+|l['\"]|un\s+|una\s+)?(.+)", "move"),
            (r"\bruota\s+(?:la\s+|l['\"]|un\s+|una\s+)?(.+)", "rotate"),
            (r"\bnascondi\s+(?:la\s+|l['\"]|un\s+|una\s+)?(.+)", "hide"),
            (r"\bmostra\s+(?:la\s+|l['\"]|un\s+|una\s+)?(.+)", "show"),
            (r"\bselziona\s+(?:la\s+|l['\"]|un\s+|una\s+)?(.+)", "select"),
        ]

        for pattern, pat_intent in verbs_patterns:
            if pat_intent != "inspect" and pat_intent != intent and intent not in ("move", "unknown"):
                continue
            m = re.search(pattern, msg_l)
            if m:
                # "creane una copia" — nessun capture group, lascia che pronome "ne" risolva
                if pat_intent == "duplicate-nocap":
                    return None
                raw = m.group(1)
                if raw:
                    # Prendi parole finché non trovi una bound word
                    parts = raw.strip(".,;:!?").split()
                    name_parts = []
                    for p in parts:
                        p = p.strip(".,;:!?\"'")
                        if not p:
                            continue
                        if p in bound_words:
                            break
                        if re.match(r"^[-\d.]+$", p) and not name_parts:
                            continue  # skip leading numbers
                        name_parts.append(p)
                        if len(name_parts) >= 3:
                            break
                    if name_parts:
                        candidate = " ".join(name_parts)
                        if candidate.lower() != "la" and len(candidate) > 1:
                            return candidate

        return None

    _PRONOUN_MAP = {
        "lo": "last_referenced_object", "la": "last_referenced_object",
        "ne": "last_referenced_object", "le": "last_referenced_object",
        "li": "last_referenced_object",
        "quello": "last_referenced_object", "quella": "last_referenced_object",
        "quelli": "last_created_object", "quelle": "last_created_object",
        "la copia": "last_created_object", "quella copia": "last_created_object",
        "la copia che hai creato": "last_created_object",
        "la copia appena creata": "last_created_object",
        "copia": "last_created_object",
        "questa": "last_created_object", "questo": "last_referenced_object",
        "l'oggetto": "last_referenced_object",
    }

    def _resolve_references(self, entities: dict, intent: str) -> dict:
        """Risolve pronomi/referimenti usando lo stato conversazione."""
        resolved = dict(entities)
        obj_name = entities.get("object_name")

        # Se nessun nome esplicito, prova pronome o contesto
        if not obj_name:
            # Check for pronouns in the original message
            msg_l = self.state.history[-1]["message"].lower()
            for pronoun, ref_field in self._PRONOUN_MAP.items():
                if pronoun in msg_l:
                    ref_val = getattr(self.state, ref_field, None)
                    if ref_val:
                        resolved["object_name"] = ref_val
                        break

            # Fallback contestuale per intento
            if not resolved.get("object_name"):
                if intent == "duplicate":
                    resolved["object_name"] = (self.state.last_referenced_object or
                                                self.state.last_created_object)
                elif intent in ("move", "rotate", "hide", "show"):
                    resolved["object_name"] = (self.state.last_created_object or
                                                self.state.last_referenced_object)

        return resolved

    def _resolve_object(self, name: str) -> str | None:
        """Risolve nome oggetto: exact → case-insensitive → fuzzy unico."""
        if not name:
            return None

        name_str = str(name)

        # 0. Cache sessione
        if name_str.lower() in self.state.session_objects:
            return self.state.session_objects[name_str.lower()]

        try:
            all_objects = core_list_objects(self.state.current_blend)
            names = [o["name"] for o in all_objects]

            # 1. Exact match
            if name_str in names:
                self.state.session_objects[name_str.lower()] = name_str
                return name_str

            # 2. Case-insensitive
            for n in names:
                if n.lower() == name_str.lower():
                    self.state.session_objects[name_str.lower()] = n
                    return n

            # 3. Fuzzy unico (nome contiene il target)
            candidates = [n for n in names if name_str.lower() in n.lower()]
            if len(candidates) == 1:
                self.state.session_objects[name_str.lower()] = candidates[0]
                return candidates[0]

            # 4. Reverse fuzzy (tutte le parole nel nome)
            words = name_str.lower().split()
            candidates = []
            for n in names:
                nl = n.lower()
                if all(w in nl for w in words):
                    candidates.append(n)
            if len(candidates) == 1:
                self.state.session_objects[name_str.lower()] = candidates[0]
                return candidates[0]

        except Exception:
            pass

        return None

    # ── Execution ──────────────────────────────────────

    def _execute(self, intent: str, resolved: dict) -> dict:
        """Esegue l'azione corrispondente all'intento."""
        handlers = {
            "inspect_scene": self._do_inspect_scene,
            "list_objects": self._do_list_objects,
            "inspect": self._do_inspect,
            "duplicate": self._do_duplicate,
            "move": self._do_move,
            "rotate": self._do_rotate,
            "hide": self._do_hide,
            "show": self._do_show,
            "select": self._do_select,
            "render": self._do_render,
            "undo": self._do_undo,
            "reset": self._do_reset,
            "help": self._do_help,
            "unknown": self._do_help,
        }

        handler = handlers.get(intent, self._do_help)
        result = handler(resolved)

        # Aggiorna stato
        if result.get("status") == "ok":
            if result.get("last_object"):
                self.state.last_referenced_object = result["last_object"]
            if result.get("new_object"):
                self.state.last_created_object = result["new_object"]
                self.state.last_referenced_object = result["new_object"]
            if result.get("version_id"):
                self.state.last_change_id = result["version_id"]
                self.state.last_tool_call = intent

        return result

    # ── Tool Handlers ─────────────────────────────────

    def _do_inspect_scene(self, _resolved: dict) -> dict:
        obs = core_list_objects(self.state.current_blend)
        if not obs:
            return {"status": "ok", "response": "Scena vuota."}
        by_type = {}
        for o in obs:
            by_type.setdefault(o.get("type", "?"), []).append(o)
        lines = [f"**Analisi Struttura** — {Path(self.state.current_blend).name}",
                 f"**{len(obs)} oggetti**\n"]
        for t, items in sorted(by_type.items()):
            lines.append(f"**{t}**: {len(items)}")
            for o in items[:6]:
                l = o.get("location", (0, 0, 0))
                d = o.get("dimensions", (0, 0, 0))
                lines.append(f"  . {o['name']} — pos({l[0]:.1f},{l[1]:.1f},{l[2]:.1f}) dim({d[0]:.1f},{d[1]:.1f},{d[2]:.1f})")
            if len(items) > 6:
                lines.append(f"  ... +{len(items)-6}")
        self.state.last_tool_call = "inspect_scene"
        return {"status": "ok", "response": "\n".join(lines)}

    def _do_list_objects(self, _resolved: dict) -> dict:
        obs = core_list_objects(self.state.current_blend)
        if not obs:
            return {"status": "ok", "response": "Nessun oggetto."}
        lines = [f"**Oggetti ({len(obs)}):**\n"]
        for o in obs:
            h = " [nascosto]" if o.get("hide_viewport") else ""
            lines.append(f"  - {o['name']} ({o['type']}){h}")
        self.state.last_tool_call = "list_objects"
        return {"status": "ok", "response": "\n".join(lines)}

    def _do_inspect(self, resolved: dict) -> dict:
        name = resolved.get("object_name")
        if not name:
            return {"status": "ok", "response": "Quale oggetto? Prova 'Analizza Tastiera'."}

        # Risolvi nome oggetto
        resolved_name = self._resolve_object(name)
        if not resolved_name:
            try:
                all_obs = core_list_objects(self.state.current_blend)
                for o in all_obs:
                    if name.lower() in o["name"].lower():
                        resolved_name = o["name"]
                        break
            except Exception:
                pass

        if not resolved_name:
            return {"status": "ok", "response": f"Oggetto **{name}** non trovato nella scena."}

        # Esegui inspect
        obj = core_inspect_object_detail(self.state.current_blend, resolved_name)
        if "error" in obj:
            return {"status": "ok", "response": f"Oggetto **{resolved_name}** non trovato durante l'ispezione."}

        # VERIFICA: l'oggetto restituito è quello richiesto?
        returned_name = obj.get("name", "")
        if returned_name and returned_name.lower() != resolved_name.lower():
            return {"status": "ok",
                    "response": f"⚠️ Conflitto: richiesto {resolved_name}, ispezionato {returned_name}. Annullo."}

        self.state.last_referenced_object = returned_name

        lines = [f"**{returned_name}** ({obj.get('type', '?')})"]
        for k, l in [("location", "Pos"), ("rotation", "Rot"),
                      ("scale", "Scale"), ("dimensions", "Dim")]:
            v = obj.get(k, (0, 0, 0))
            lines.append(f"  {l}: ({v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f})")
        if obj.get("parent"):
            lines.append(f"  Padre: {obj['parent']}")
        if obj.get("children"):
            lines.append(f"  Figli: {', '.join(obj['children'][:10])}")
        if obj.get("materials"):
            lines.append(f"  Materiali: {', '.join(obj['materials'])}")
        if obj.get("vertex_count"):
            lines.append(f"  Vertici: {obj['vertex_count']}")
            lines.append(f"  Facce: {obj['face_count']}")
            lines.append(f"  Spigoli: {obj['edge_count']}")
        if obj.get("hide_viewport"):
            lines.append("  (nascosto)")

        self.state.last_tool_call = "inspect"
        return {"status": "ok", "response": "\n".join(lines), "last_object": returned_name}

    def _do_duplicate(self, resolved: dict) -> dict:
        name = resolved.get("object_name")
        if not name:
            return {"status": "ok", "response": "Quale oggetto vuoi duplicare?"}

        resolved_name = self._resolve_object(name)
        if not resolved_name:
            return {"status": "ok", "response": f"Oggetto **{name}** non trovato."}

        new_name = f"{resolved_name}_copia"

        try:
            r = safe_operate(
                self.state.current_blend,
                core_duplicate_object,
                [resolved_name, new_name],
                description=f"Duplica {resolved_name}",
                user_request="",
            )
            self.state.current_blend = r["version_path"]
            self.state.last_created_object = new_name
            self.state.last_referenced_object = new_name
            self.state.last_change_id = r["version_id"]
            self.state.session_objects[new_name.lower()] = new_name
            self.state.session_objects["copia"] = new_name

            return {
                "status": "ok",
                "response": f"✅ Creata copia **{new_name}** da **{resolved_name}**\nVersione: {r['version_id']}",
                "new_object": new_name,
                "version_id": r["version_id"],
                "last_object": new_name,
            }
        except Exception as e:
            return {"status": "ok", "response": f"❌ Errore duplicazione: {e}"}

    def _do_move(self, resolved: dict) -> dict:
        name = resolved.get("object_name")
        if not name:
            return {"status": "ok", "response": "Quale oggetto vuoi spostare?"}

        resolved_name = self._resolve_object(name)
        if not resolved_name:
            return {"status": "ok", "response": f"Oggetto **{name}** non trovato."}

        if "coordinates" in resolved:
            x, y, z = resolved["coordinates"]
        elif "direction" in resolved:
            offset = resolved["numbers"][0] if resolved.get("numbers") else 1.0
            dir_map = {
                "right": (1, 0, 0), "left": (-1, 0, 0),
                "up": (0, 0, 1), "down": (0, 0, -1),
                "forward": (0, 1, 0), "backward": (0, -1, 0),
            }
            d = dir_map.get(resolved["direction"], (1, 0, 0))
            try:
                cur = core_inspect_object_detail(self.state.current_blend, resolved_name)
                if "error" not in cur:
                    cl = cur.get("location", (0, 0, 0))
                    x = float(cl[0]) + d[0] * offset
                    y = float(cl[1]) + d[1] * offset
                    z = float(cl[2]) + d[2] * offset
                else:
                    return {"status": "ok", "response": f"Oggetto **{resolved_name}** non trovato."}
            except Exception:
                return {"status": "ok", "response": f"Oggetto **{resolved_name}** non trovato."}
        else:
            return {"status": "ok", "response": "Specifica dove spostarlo. Es: 'Sposta Tastiera verso destra di 2'"}

        try:
            r = safe_operate(
                self.state.current_blend,
                core_move_object,
                [resolved_name, x, y, z],
                description=f"Sposta {resolved_name}",
                user_request="",
            )
            self.state.current_blend = r["version_path"]
            self.state.last_change_id = r["version_id"]
            dir_label = resolved.get("direction", "")
            dir_text = f" verso {dir_label}" if dir_label else ""
            return {
                "status": "ok",
                "response": f"✅ **{resolved_name}** spostato{dir_text}\n({x:.1f}, {y:.1f}, {z:.1f})\nVersione: {r['version_id']}",
                "version_id": r["version_id"],
                "last_object": resolved_name,
            }
        except Exception as e:
            return {"status": "ok", "response": f"❌ Errore spostamento: {e}"}

    def _do_rotate(self, resolved: dict) -> dict:
        name = resolved.get("object_name")
        if not name:
            return {"status": "ok", "response": "Quale oggetto vuoi ruotare?"}
        resolved_name = self._resolve_object(name)
        if not resolved_name:
            return {"status": "ok", "response": f"Oggetto **{name}** non trovato."}
        angle = resolved.get("angle", 45)
        rad = math.radians(angle)
        try:
            r = safe_operate(
                self.state.current_blend,
                core_rotate_object,
                [resolved_name, 0, 0, rad],
                description=f"Ruota {resolved_name} {angle}°",
                user_request="",
            )
            self.state.current_blend = r["version_path"]
            self.state.last_change_id = r["version_id"]
            return {"status": "ok",
                    "response": f"✅ **{resolved_name}** ruotato {angle}° su Z\nVersione: {r['version_id']}",
                    "version_id": r["version_id"], "last_object": resolved_name}
        except Exception as e:
            return {"status": "ok", "response": f"❌ Errore rotazione: {e}"}

    def _do_hide(self, resolved: dict) -> dict:
        name = resolved.get("object_name")
        if not name:
            return {"status": "ok", "response": "Quale oggetto nascondere?"}
        resolved_name = self._resolve_object(name)
        if not resolved_name:
            return {"status": "ok", "response": f"Oggetto **{name}** non trovato."}
        try:
            r = safe_operate(self.state.current_blend, core_hide_object,
                             [resolved_name], "Nascondi", "")
            self.state.current_blend = r["version_path"]
            self.state.last_change_id = r["version_id"]
            return {"status": "ok", "response": f"✅ **{resolved_name}** nascosto\nVersione: {r['version_id']}",
                    "version_id": r["version_id"], "last_object": resolved_name}
        except Exception as e:
            return {"status": "ok", "response": f"❌ {e}"}

    def _do_show(self, resolved: dict) -> dict:
        name = resolved.get("object_name")
        if not name:
            return {"status": "ok", "response": "Quale oggetto mostrare?"}
        resolved_name = self._resolve_object(name)
        if not resolved_name:
            return {"status": "ok", "response": f"Oggetto **{name}** non trovato."}
        try:
            r = safe_operate(self.state.current_blend, core_show_object,
                             [resolved_name], "Mostra", "")
            self.state.current_blend = r["version_path"]
            self.state.last_change_id = r["version_id"]
            return {"status": "ok", "response": f"✅ **{resolved_name}** visibile\nVersione: {r['version_id']}",
                    "version_id": r["version_id"], "last_object": resolved_name}
        except Exception as e:
            return {"status": "ok", "response": f"❌ {e}"}

    def _do_select(self, resolved: dict) -> dict:
        name = resolved.get("object_name")
        if not name:
            return {"status": "ok", "response": "Quale oggetto selezionare?"}
        resolved_name = self._resolve_object(name)
        if not resolved_name:
            return {"status": "ok", "response": f"Oggetto **{name}** non trovato."}
        try:
            r = safe_operate(self.state.current_blend, core_select_object,
                             [resolved_name], "Seleziona", "")
            self.state.current_blend = r["version_path"]
            self.state.last_change_id = r["version_id"]
            return {"status": "ok", "response": f"✅ **{resolved_name}** selezionato\nVersione: {r['version_id']}",
                    "version_id": r["version_id"], "last_object": resolved_name}
        except Exception as e:
            return {"status": "ok", "response": f"❌ {e}"}

    def _do_render(self, _resolved: dict) -> dict:
        ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d-%H%M%S")
        out_name = f"preview_{ts}.png"
        out = core_render_preview(self.state.current_blend, out_name, 1280, 720, 32, 1, 600)
        self.state.last_tool_call = "render"
        return {"status": "ok",
                "response": f"🎬 Render pronto!",
                "render_path": out,
                "render_url": f"/render-file/{out_name}"}

    def _do_undo(self, _resolved: dict) -> dict:
        v = sorted(get_versions_dir().glob("[0-9][0-9][0-9][0-9].blend"))
        if len(v) < 2:
            return {"status": "ok", "response": "Nessuna versione precedente per undo."}
        prev = v[-2]
        new_p, meta = core_duplicate_version(str(prev), "Undo")
        self.state.current_blend = new_p
        self.state.last_change_id = meta.version_id
        return {"status": "ok",
                "response": f"↩️ Undo: ripristinata versione {prev.stem}\nNuova versione: {meta.version_id}",
                "version_id": meta.version_id}

    def _do_reset(self, _resolved: dict) -> dict:
        self.reset()
        return {"status": "ok", "response": "🔄 Conversazione resettata."}

    def _do_help(self, _resolved: dict = None) -> dict:
        return {"status": "ok", "response":
            "**Cosa posso fare:**\n\n"
            "🔍 **Ispezionare**\n"
            "  • 'Analizza la struttura' — tutta la scena\n"
            "  • 'Analizza Tastiera' — dettagli di un oggetto\n\n"
            "✏️ **Modificare**\n"
            "  • 'Crea una copia di Tastiera'\n"
            "  • 'Sposta Sgabello verso destra di 2'\n"
            "  • 'Ruota Sgabello di 45'\n"
            "  • 'Nascondi Sgabello' / 'Mostra Sgabello'\n\n"
            "🎬 **Render e versioni**\n"
            "  • 'Fammi vedere il risultato' — render\n"
            "  • 'Annulla' o 'Torna indietro' — undo\n\n"
            "💡 **Riferimenti**\n"
            "  Dopo aver parlato di un oggetto, puoi usare:\n"
            "  'ne', 'la', 'lo', 'quello' — si riferiscono all'ultimo oggetto\n"
            "  'copia', 'la copia' — si riferisce all'ultima copia creata"}