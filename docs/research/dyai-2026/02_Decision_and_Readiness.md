# DYAI – Decision Memo & Product Investment Readiness
**Stand: 11.10.2026 · PARTIAL_EVIDENCE · interne Arbeitsunterlage**

## A. Executive Decision Memo

**Empfehlung:** Drei getrennte Angebote statt einer „DYAI-Suite“: **Plumbline**, **ASM**, **PXAPI**. Die Auswahl ist eine evidenzbasierte Vermarktungsempfehlung, keine Bestätigung von Product-Market-Fit. Von diesen dreien sind zwei enge lokale Funktionspfade reproduziert; PXAPI bleibt bis zur Laufzeitprüfung ein bedingtes Angebot.

**Plumbline** hat die stärkste vorläufige Venture-These: eine Anforderung darf nicht mit unzureichenden Nachweisen als erledigt gelten. Die Python-/CLI-Implementierung wurde gelesen, 77 Assertions bestanden, und das CLI wies eine `fake-only`-Fixture mit Exit 3 zurück, während eine passende Integrations-Fixture Exit 0 lieferte. Das ist eine **lokal verifizierte Policy-Demo**, kein Nachweis universeller semantischer Richtigkeit. Agent Team und ASM sind nicht als integrierte Bestandteile nachgewiesen. Zuerst einen bezahlten Engineering-Pilot anbieten; parallel qualifizierende Investorengespräche führen.

**ASM** ist der beste sichtbare Produkt-/Design-Partner-Kandidat. 706 Tests, Typecheck, Produktvalidierung und Build bestanden. Im lokal gestarteten Produkt wurden Lesen, explizite Freigabe, YAML-Export und Ablehnung einer nicht vorhandenen Persona über HTTP reproduziert. Das lokale Frontend liefert HTML; eine vollständige Browser-Interaktion und reale KI-Ausgabe wurden nicht überprüft. Vermarkten: menschlich freigegebener, maschinenlesbarer Produktkontext. Nicht vermarkten: autonome Discovery oder bereits integrierte Software-Delivery. Ein Pilot muss zeigen, ob die kanonische Struktur Übergabefehler gegenüber dem bisherigen Prozess tatsächlich reduziert.

**PXAPI** ist eher ein kurzfristig verkaufbarer Diagnosekern als bereits ein VC-Unternehmen. Implementiert sind statische Homepage-Analyse, getrennte Discovery-/Acquisition-CLI-Pfade und eine Evidenzkette von Finding zu Messung. Die lokale Ausführung scheitert vorerst an der Beschaffung des erforderlichen Python ≥3.13. Deshalb nur einen bedingten Pilot-/Evaluationsumfang besprechen, keine einsatzfertige API-Lizenz zusagen. Eine standardisierte Dienstleistung kann wirtschaftlich besser passen als ein Venture-finanziertes SaaS.

**Nicht jetzt als Investment-Lead:** DESTILL Design benutzt synthetische Analyse-/Schnittplan-Daten; der Produktionsadapter meldet auch Video Understanding als `NOT_IMPLEMENTED`. Der Backend-Code ist nicht zugänglich. FuFirE hat konkrete Berechnungsfunktionen, aber Nischenökonomie, astronomische vs. astrologische Aussagekraft und Swiss-Ephemeris-Rechte müssen getrennt geprüft werden. Semantic Brain Graph und Agent Team sind `UNVERIFIED`. Der zusätzlich gefundene Website-Diagnosis-Agent ist ausdrücklich ein Repository ohne Produktimplementierung.

**Echte Demo-Voraussetzungen:** Plumbline braucht einen klar begrenzten Fixture-Fall; ASM eine isolierte Produktdatei und eine sichtbare Kennzeichnung fehlender Live-KI; PXAPI eine kompatible Laufzeit und genau einen nachvollziehbaren Analysefall. Nicht erforderlich sind gemeinsame Plattform, Billing, autonome Agentenflotte, Enterprise-Skalierung oder automatische Videorendering-Pipeline. Authentifizierung und Datentrennung bleiben jedoch Release-Blocker, sobald echte Kundendaten verarbeitet werden.

**Kapitalstrategie:** Keine erfundene Runde. Benötigt werden tatsächliche Founder-Verfügbarkeit, Entwicklungs-/Vertriebskosten, Cloud-/Modellbudget, Rechts-/Lizenzkosten, Runway und Zielmeilenstein. Fundraising sollte eine konkrete Produktthese finanzieren, nicht die Repository-Sammlung.

**Wichtigstes Risiko:** Technische Aktivität wird mit kaufbarem Nutzen und exklusiv verwertbarer IP verwechselt. Die schnellere Gegenprobe ist ein bezahlter, begrenzter Vergleichspilot mit vereinbartem Abnahmekriterium. Ein Testlauf beweist Funktion, eine freundliche Antwort Interesse; erst ein Auftrag oder eine Zahlung belegt Zahlungsbereitschaft.

## B. Product Investment Readiness Matrix

Alle GitHub-Belege beziehen sich auf die unten eingefrorenen Commits. README-Inhalte sind Entwicklerangaben; nur die unter „Ausführung“ genannten Vorgänge wurden selbst ausgeführt.

| Produkt | Zielmarkt / Käuferhypothese | Bestehende Funktion | Demo-Evidenz | Fehlender Kern / Evidenz | IP-Status | Investment-Hypothese | Nächster Schritt |
|---|---|---|---|---|---|---|---|
| Plumbline | Engineering-Leitung, Platform-/DevEx-Team | Reality-/Context-/Scope-Checks, CLI, Rollen-/Workflow-Artefakte | **LOCAL_DEMO_VERIFIED**, nur deterministisches CLI mit synthetischen Fixtures | Wiederholbarer inkrementeller Nutzen gegenüber Reviews; Live-Watcher nicht unabhängig geprüft | MIT; ausdrücklich claude-flow-Ableitungen; Gesellschaftszuordnung UNKNOWN | Reliability-Layer für agentische Softwareentwicklung; Moat erst zu zeigen | Begrenzten bezahlten Review-Vergleich anbieten |
| ASM | Head of Product / Product Ops / Delivery-Leitung | Kanonisches Modell, Story Map, Freigabe, Datei-Persistenz, Import/Export, Proposal-Code | **LOCAL_DEMO_VERIFIED**, HTTP-Kern; Browser- und KI-E2E nicht geprüft | Live-Provider-Qualität, Team-Adoption, echte Übergabe in Delivery | Keine Root-LICENSE gefunden; Rechtekette/Gesellschaft UNKNOWN | Produktkontext als kontrollierte Schnittstelle zwischen Mensch und Agent | Einen Discovery-to-Engineering-Pilot mit Ausgangsvergleich |
| Agent Team | Engineering-Orchestrierung als Hypothese | **UNKNOWN** | **UNVERIFIED** | Zugriff auf Implementierung fehlt | UNKNOWN | Keine belastbare gegenwärtige These | Zugriff qualifizieren; nicht in Plumbline-Umsatzthese hineinrechnen |
| DESTILL Backend | Creator-/Medienproduktion | **UNKNOWN**, Zugriff 403 | **UNVERIFIED** | Reales Verstehen, Audio-/Videoverarbeitung, Export nicht prüfbar | UNKNOWN | Potenzielles Creator-Werkzeug, nicht belegt | Backend-Zugriff und ein realer Clip-Output |
| DESTILL Design | Creator-/Editor-UX | React-Screens, lokale Dateiauswahl-/Preview-Logik, synthetische Reports und Edit-Pläne | **PARTIAL_IMPLEMENTATION**; interaktiver Prototyp laut Quellcode, nicht lokal gestartet | ProductionEngineAdapter wirft Fehler, Understanding/Prosody/Rendering nicht implementiert in diesem Repo | Keine Root-LICENSE gefunden; Mitentwicklerrechte UNKNOWN | Design-Validierung, keine fertige Automations-These | Nur als synthetisch gekennzeichneten UX-Prototyp vorführen |
| PXAPI | Digital-/SEO-Agenturen, Website-Betreiber | Statische HTTP-Analyse, Evidenz-/Finding-Kette; CLI Discovery/Acquisition | **CODE_EVIDENCE_ONLY** | Kompatible Laufzeit hier nicht installiert; keine eigene End-to-End-Ausführung | MIT im Repo; Rechteübertragung UNKNOWN | API bei nachgewiesenem wiederkehrendem Volumen, sonst Dienstleistung | Runtime herstellen, einen autorisierten Analysefall ausführen |
| FuFirE | Betreiber kultureller/Astrologie-Apps | `compute_bazi`, `compute_fusion_analysis`, `compute_lunar_state`, FastAPI-Router | **CODE_EVIDENCE_ONLY**, Testdateien vorhanden, nicht ausgeführt | Ephemeriden-/Referenzvalidierung, Kunden-/API-Nutzungsdaten | MIT im Repo ersetzt nicht Swiss-Ephemeris-Lizenzprüfung; kommerzielle Lizenz UNKNOWN | Wiederholbare Nischen-API, eher Lizenz-/Umsatzfinanzierung | Lizenzmodell und Grenzzeitpunkte gegen unabhängige Referenzen klären |
| Semantic Brain Graph | Agent-Memory-/Knowledge-Teams als Hypothese | UNKNOWN | **UNVERIFIED** | Code, Datenmodell, Retrieval, Löschung, Integration nicht zugänglich | UNKNOWN | Infrastrukturmarkt vorhanden, DYAI-Differenzierung unbekannt | Keine Infrastruktur-Pitches ohne Code-/Benchmarkzugriff |
| website-diagnosis-agent | Website-Diagnose | Nur README / Projektbindung | **PARTIAL_IMPLEMENTATION** | Gesamte Produktimplementierung fehlt laut Repo und Dateibaum | UNKNOWN | Kein zusätzlicher Produktkern neben PXAPI nachgewiesen | Nicht als laufenden PXAPI-Agenten präsentieren |
| Ana-Agents | Evidenzbasierte Brand-Partnership-Outreach | Lokales Repo enthält Skills, Runtime-/Policy-/Schema-/Teststruktur; keine vertiefte Laufzeitprüfung in dieser Recherche | **UNVERIFIED** als vermarktbares Produkt | Kommerzielle Nutzung, externe Adapter und End-to-End-Betrieb nicht geprüft | Separate IP-/Lizenzprüfung nötig | Eher interne Infrastruktur als zusätzliche unmittelbare These | Für Governance nutzen, nicht als Marktbeweis zählen |

### Eingefrorene technische Quellen
| Kürzel | Repository und Commit | Direkt geprüfte Stellen |
|---|---|---|
| T1 | [Plumbline `9bb058c8ecf661226d1a9ca22e7a0ea1914ffef6`](https://github.com/DYAI2025/Plumbline/tree/9bb058c8ecf661226d1a9ca22e7a0ea1914ffef6) | `config/claude/lib/plumbline_reality.py`, `config/claude/tests/test_runtime_integrity_layer.sh`, PRIL-Fixtures, LICENSE |
| T2 | [ASM `25dcd760d0f7a357e2cdb086b9980fce452538f0`](https://github.com/DYAI2025/ASM-Agentic-Story-Mapping/tree/25dcd760d0f7a357e2cdb086b9980fce452538f0) | `src/domain/validate.ts`, `src/app/api/product/route.ts`, `product/approve/route.ts`, `proposal/route.ts`, package.json, Tests |
| T3 | [DESTILL Design `ad56afb268761d1cbad20ec108aa5865017e6765`](https://github.com/DYAI2025/ANA-CapCut-AI-DESIGN/tree/ad56afb268761d1cbad20ec108aa5865017e6765) | `src/services/engineAdapter.ts` insb. ProductionEngineAdapter ab Zeile 425, `src/lib/store.tsx`, package.json |
| T4 | [PXAPI `ce4de1820d2516f9b3bf73b11ad9441dbad941ba`](https://github.com/DYAI2025/PXAPI-Analyse-API/tree/ce4de1820d2516f9b3bf73b11ad9441dbad941ba) | `src/pxapi/application/analyze_homepage.py`, `adapters/inbound/`, `tests/adapters/`, pyproject.toml, LICENSE |
| T5 | [FuFirE `8ad7dce62db5393654d27f2f2060a0ca644aa2b6`](https://github.com/DYAI2025/FUFIRE_API_lunar/tree/8ad7dce62db5393654d27f2f2060a0ca644aa2b6) | `bazi_engine/cli.py`, `app.py`, Berechnungsfunktionen in bazi.py, fusion.py, lunar_state.py, LICENSE |
| T6 | [Website Diagnosis `66ed04ad3878cbe8d1bccd4c549d8ab269048361`](https://github.com/DYAI2025/website-diagnosis-agent/tree/66ed04ad3878cbe8d1bccd4c549d8ab269048361) | README und Dateibaum: kein Produktcode |
| T7 | [Ana-Agents `96f01c0019e2f3e088be6aeb78c25ee002a48b28`](https://github.com/DYAI2025/Ana-Agents/tree/96f01c0019e2f3e088be6aeb78c25ee002a48b28) | AGENTS.md, README, Dateibaum; keine eigenständige Readiness-Prüfung |

### Ausführung und Evidenzgrenzen
- **Plumbline:** `bash config/claude/tests/test_runtime_integrity_layer.sh`, Exit 0, **77 Assertions / 0 fehlgeschlagen**. Ein Teil prüft Artefakte, ein Teil Verhalten. Nicht als 77 unabhängige Produkt-/Kundentests zählen. Zusätzlich direktes `plumbline-reality-check`: fake-only Exit 3, integration-pass Exit 0. Logs: `plumbline-runtime.txt`, `plumbline-cli-demo.json`.
- **ASM:** `npm ci --ignore-scripts` Exit 0; `npm test` Exit 0, **47 Dateien / 706 Tests**; `npm run validate`, `npm run typecheck`, `npm run build` erfolgreich. Keine bezahlten Modellaufrufe. Playwright-E2E nicht ausgeführt; vorhandene E2E-Konfiguration setzt Fake-/Stub-Provider.
- **ASM HTTP-Demo:** GET Produkt 200 → explizite Freigabe 200 → YAML-Export 200 → ungültige Persona `nonexistent-research-persona` führt zu 422 / `unknown_persona`. `/` liefert HTML 200. Zuvor separat eine ungültige ID-Syntax getestet: ebenfalls 422, aber **Schemafehler**, nicht Referenznachweis. Beide Fälle sauber getrennt in `asm-http-demo.json` und `asm-reference-demo.json`.
- **ASM Datengrenze:** Nur Kopie der öffentlichen Produkt-Fixture; „Research demo (synthetic approver)“ ist keine echte geschäftliche Freigabe. Kein Auth-/Mandantenschutz für Kundennutzung geprüft. Keine echten Daten in eine öffentliche Preview laden.
- **PXAPI:** Python 3.11 vorhanden, Projekt verlangt ≥3.13,<3.15. `uv sync` Exit 2 wegen Interpreter-Download/TLS; zweiter Versuch mit Systemzertifikaten ebenfalls Exit 2. **Keine PXAPI-Tests ausgeführt.** Keine Projektanforderung abgeschwächt, kein Fake-Erfolg.
- Keine öffentliche Live-Demo wurde funktional verifiziert. Ein Link auf einen Agent Explorer ist kein Beweis der agentischen Laufzeit.

## Sechs Produktthesen – kommerzielle Gegenprobe

### 1. Agentic Software Delivery Reliability
**FACT:** Plumbline besitzt ausführbare Checks und dokumentierte Workflows. **SUPPORTED_INFERENCE:** Ein Engineering-Team kann ein explizites Mindestniveau an Nachweisen erzwingen. **HYPOTHESIS:** Das reduziert Fehlfreigaben zu vertretbaren Reviewkosten. **UNKNOWN:** Installationen, aktive Nutzer, zahlende Kunden, Effektgröße.

**Kein integriertes Produkt:** Agent Team nicht lesbar; keine überprüfte Verbindung zu ASM. Ein „Plumbline + ASM + Agent Team“-Diagramm wäre nur Zielarchitektur. Vorläufig separat verkaufen.

**Käufer/Budget:** CTO, VP Engineering, Platform-/DevEx-Leitung. **Erlösmodell-Hypothese:** Fixpreis-Evaluation, danach Team-/Repository-Lizenz plus Support. MIT-Basis ist kein Hindernis für Umsatz, aber kein exklusiver Code-Moat. Nachhaltige Verteidigbarkeit müsste aus Integration, vertrauenswürdigen Evaluationsdaten, Workflows und Distribution entstehen.

### 2. AI-native Product Discovery
**FACT:** ASM hält referenziertes Produktwissen und explizite Freigaben in einer Datei. **HYPOTHESIS:** Weniger Kontextverlust beim Übergang von Discovery zu Umsetzung. **Käufer/Budget:** Head of Product, Product Ops oder Delivery-Verantwortliche. **Erlös:** zunächst bezahlter Workshop/Pilot; später Workspace-/Team-Lizenz, falls unabhängige Teams wiederholt zurückkehren. Copy-paste aus einem Gespräch ist keine automatische Jira-/Engineering-Integration.

### 3. Creator Intelligence / DESTILL
**FACT:** Code der Designseite führt synthetische Understanding-Reports und Edit-Pläne; Produktion nicht implementiert. **UNKNOWN:** tatsächliche Backend-Fähigkeiten. **Käufer:** Creator-Agenturen, Video-Editoren, Medienproduktion. Erst UX-/Problemvalidierung; kein Pitch „automatischer Videoschnitt funktioniert“. [Descript](https://www.descript.com/) bietet bereits textbasiertes Editing und AI-Co-Editing laut eigener Produktseite (Abruf 11.10.2026). DYAI müsste einen nachvollziehbaren Vorteil in Auswahlentscheidungen, lokalem Workflow oder Rechte-/Datenschutz zeigen – derzeit Hypothesen, keine Überlegenheit.

### 4. FuFirE / Vertical API
**FACT:** Berechnungsfunktionen und API-Struktur existieren. Gleiche Eingaben / stabile Berechnungen sind ein testbares technisches Ziel, **keine** wissenschaftliche Validierung astrologischer Persönlichkeits- oder Lebensprognosen. Kulturelle Relevanz für BaZi-/Astrologie-Produkte ist eine Markthypothese; sie belegt weder globale Zahlungsbereitschaft noch einen großen VC-Markt.

**Lizenzrisiko:** [Astrodienst](https://www.astro.com/swisseph/swephinfo_e.htm) beschreibt AGPL oder Professional License, Wahl vor Distribution bzw. öffentlichem Dienst. FuFirEs MIT-Datei belegt keine erworbene Professional License und löst keine Abhängigkeitsrechte. Juristisch prüfen, bevor ein proprietärer öffentlicher API-Betrieb oder exklusive IP behauptet wird. **Nächster Nachfragetest:** Ein existierender App-Betreiber vergleicht Grenzfälle und fragt ein reales Nutzungsvolumen an; Jahres-Mindestabnahme statt generischer TAM-Folie.

### 5. Website Intelligence / PXAPI
**FACT:** Der technische Fehler wird im Code nicht zur negativen Aussage über die Website gemacht. **HYPOTHESIS:** Agenturen zahlen für geringere manuelle Nachprüfung und bessere Belegbarkeit gegenüber Kunden. **Grenze:** Messbare HTML-/Indexability-Befunde sind keine Unternehmensbewertung, kein Conversion-Uplift und keine Garantie für Such-/KI-Sichtbarkeit.

**Geschäftsform entscheiden:** Dienstleistung, wenn Scope und Interpretation je Kunde individuell bleiben. Technologiegestützte Agentur, wenn Umsetzung/Consulting den Deckungsbeitrag tragen. Softwareunternehmen erst, wenn standardisierte wiederkehrende Nutzung, geringe variable Betreuung und wiederholbarer Vertrieb erkennbar werden. Das Produkt nicht künstlich zu VC-SaaS erklären.

### 6. Agent Memory / Semantic Brain Graph
**UNKNOWN:** DYAI-Code, semantisches Modell, Tenant-Isolation, Datenlöschung, Wiederaufnahme über Sessions, Integrationen und technische Eigenständigkeit. [Zep](https://www.getzep.com/) vermarktet Context Graphs, Policy-Zugriff und Quellenverknüpfung; [Mem0](https://mem0.ai/) persistente Agent-Memory (Abruf 11.10.2026, Anbieterclaims, keine unabhängigen Benchmarks). „Memory“ allein ist keine Differenzierung. Bis Zugriff und Vergleichsdaten vorliegen nicht priorisieren.

## Wettbewerb für die drei Prioritäten
| Produkt | Konkrete Alternative / offizieller Beleg | Was DYAI glaubwürdig unterscheiden kann | Was noch nicht behauptet werden darf |
|---|---|---|---|
| Plumbline | [Braintrust](https://www.braintrust.dev/): Observability, Evals, Releases; [LangSmith](https://www.langchain.com/langsmith/observability): Agent-Tracing; [Thoughtworks](https://www.thoughtworks.com/en-de/what-we-do/ai): Agent/works Governance | Enge, repositorynahe Prüfung der Eignung deklarierter Nachweise gegen Anforderungen als Positionierung | „Einziges Tool“, allgemein bessere Qualität, vollständige semantische Korrektheit; die Alternativen haben überschneidende Funktionen |
| ASM | [Miro AI](https://miro.com/ai/ai-overview/): Canvas-Kontext, Sidekicks, Workflows; [Productboard](https://www.productboard.com/platform/): Kundenbedarf, Priorisierung, Roadmaps | Kanonische lokal gespeicherte Produktdatei und explizite Freigabe als kontrollierter Übergabepunkt | Dass Wettbewerber keine strukturierten Modelle oder KI haben; dass lokale Architektur automatisch vollständige Datenhoheit garantiert |
| PXAPI | [Screaming Frog](https://www.screamingfrog.co.uk/seo-spider/): Crawling, SEO-/UX-Checks, JavaScript-Rendering; [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview): automatisierte Performance-/Accessibility-/SEO-Audits und CI | Besonders explizite Finding→Evidenz→Messung-Kette und Unknown-Semantik; Nutzen muss im Workflowvergleich bewiesen werden | Breitere Abdeckung, besseres SEO, mehr Umsatz oder einzigartige Auditfähigkeit |

Abruf aller Wettbewerberseiten: 11.10.2026; undatierte Produktseiten haben **Publikationsdatum UNKNOWN**. Anbieterkennzahlen wurden nicht auf DYAI übertragen. Kein extern belegter TAM wurde ermittelt. Marktgröße vorläufig bottom-up kalkulieren: adressierbare Teams × tatsächliche Wiederkaufrate × validierter jährlicher Vertragswert; alle drei Inputs noch UNKNOWN.

## Governance / Investierbarkeit – vor externer Zusage
1. **MARKETING_BLOCKER:** Rechtlicher Absender, Gesellschaft, Gründungsdatum, wirtschaftlich Berechtigte, Cap Table, verfügbare Founder-Zeit und Rollen fehlen. GitHub-Owner ist kein Handelsregisterbeleg.
2. **MARKETING_BLOCKER:** Contributor-/Auftragsverhältnisse, Rechteübertragung, Drittbibliotheken und mögliche Kundendaten-/Code-Rechte dokumentieren. Root-LICENSE ≠ lückenlose Rechtekette.
3. **MARKETING_BLOCKER:** Produktumfang und Demo-Evidenz ausdrücklich freigeben. Confluence-Governance kann nicht durch neue Marketingtexte ersetzt werden.
4. **RELEASE_BLOCKER:** Security, Auth, Tenant-Isolation, Backups, Datenschutz, Logging/Retention und Betriebsverantwortung vor echten produktiven Daten prüfen – nicht für eine isolierte öffentliche Fixture-Demo alles neu bauen.
5. **DEFERRED:** Gemeinsames Billing, Marketplace, Multi-Produkt-Vertrieb und internationale Gesellschaftsstruktur bis konkrete Kunden-/Investoranforderung vorliegt.
6. Finanzierung: Bedarf = nachvollziehbare monatliche Vollkosten × vereinbarte Runway + Einmalkosten + begründete Reserve − tatsächlich verfügbare Mittel. Kein Betrag, keine Bewertung und kein Ticket-Fit ohne diese Daten.

## Geografische Suchabdeckung und bewusste Lücken
- Deutschland/UK/übriges Europa und USA: konkrete Fonds anhand offizieller Thesen, Team-/Kontaktseiten und teilweise 2025/26-Deals geprüft; siehe Register. DACH ist kein garantierter Deal-Zugang, nur der geringste erkennbare Strukturierungsaufwand.
- Israel: Angular weist ausdrücklich Europa/Israel aus. Singapur/Indien: Crane hat entsprechende Partner/Standorte, relevant bleibt zunächst die Europa-Route, nicht eine künstliche APAC-Struktur.
- [BEENEXT](https://www.beenext.com/beliefs/): Japan-/Indien-/SEA-/US-Fokus in Partnerprofilen; Zulässigkeit eines deutschen Unternehmens nicht belegt. **B – QUALIFICATION_NEEDED**, nicht zur qualifizierten Shortlist gezählt.
- [Wamda Capital](https://wamdacapital.com/): Gesellschaft, Team und Evergreen-Modell verifiziert; aktueller DYAI-Sektor-/Deutschland-Fit und eigene jüngste Runde nicht hinreichend geprüft. **C – LOW_FIT für unmittelbare Priorisierung**, kein harter Ausschluss behauptet.
- [Airtree FAQ](https://www.airtree.vc/faq): Fokus auf Aussie/Kiwi-Gründer, Auslandsfälle mit ANZ-Verbindung bzw. globale Marktführer mit Australienexpansion. Eine solche DYAI-Verbindung ist UNKNOWN. **C – LOW_FIT**, nicht EXCLUDED, weil Founder-Hintergrund nicht bekannt.
- Kanada, Irland separat, Südkorea und weitere Golfstaaten: **SOURCE_NEEDED**, keine ausreichende qualifizierte Suche in diesem Pass. Japan/Indien nur oberflächlich gescreent. Diese Arbeit ist ausdrücklich **keine abgeschlossene weltweite 30–50-Fonds-Recherche**.
- Angels: Keine Person wurde allein wegen Bekanntheit oder Fund-LP-Status als aktuell investierender Angel qualifiziert. Founder-Netzwerke über Fonds sind mögliche spätere Intro-Pfade, keine vorhandenen warmen Intros.

## Adversariale Schlussprüfung
1. **Investierbar oder Dienstleistung?** Plumbline/ASM sind mögliche skalierbare Produkte, noch ohne wirtschaftlichen Beweis; PXAPI zunächst Dienstleistungs-/Pilotlogik.
2. **Aktiv oder historisch?** Eigene aktuelle Deals nur dort gewertet, wo Beteiligung belegt; Portfolio-News, Fundlaunch und offene Bewerbung sind separat markiert.
3. **Spezifisch?** Jeder Registereintrag ist Plumbline oder ASM zugeordnet. PXAPI wird nicht zur Verbesserung des VC-Fits umetikettiert.
4. **Unternehmensphase?** Pre-seed/inception ist häufig belegt; Solo-Founder-Akzeptanz und konkrete DYAI-Gesellschaft bleiben meist offen. Darum keine pauschalen A-Leads.
5. **Kontakt real?** 13 der 15 Registerkandidaten haben einen offiziellen Form-/E-Mail-/Social-Pfad; Lunar und Point Nine bleiben ohne verifizierten Pitchweg. Kein Formular wurde abgesendet.
6. **Stärkste Gegenhypothese?** Bestehende Plattformen können Features nachbauen; Teamfokus und Vertriebsfähigkeit sind wichtiger als Repository-Anzahl.
7. **Demonstrierbar?** Zwei enge lokale Pfade ja; PXAPI noch nicht. Nicht alle drei als live darstellen.
8. **Nur README?** Watcher-Wirkung, FuFirE-Test-/Performancekennzahlen, reale Backend-/Deploymentbehauptungen nicht unabhängig bestätigt.
9. **Schnellerer Zahlungsbeweis?** Ein scoped Pilot mit abnahmefähigem Bericht und bezahlter Rechnung statt vollständigem Plattformbau.
10. **Sofort nutzbar?** Kontaktwege, fünf qualifizierende Investorentexte, drei ehrliche Produktpitches, Demo-Skripte und Pilot-Angebotslogik. Nutzung vorbehaltlich Governance-/IP-Freigabe.

**Gesamtstatus: PARTIAL_EVIDENCE.** Nicht BLOCKED, weil konkrete Code- und Kontaktbelege nutzbar sind; nicht RESEARCH_COMPLETE, weil interne Strategiequellen, einige Repositories, weltweite Abdeckung und wichtige Investierbarkeitsdaten fehlen.
