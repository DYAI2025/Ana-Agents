# DYAI · Global Investor & Strategic Partner Intelligence 2026
**Entscheidungsstand: 11.10.2026 · Gesamtstatus: PARTIAL_EVIDENCE**

## Entscheidung in 30 Sekunden
1. **Plumbline zuerst:** enger CLI-Prüfpfad lokal verifiziert; bezahlten Engineering-Vergleich vorbereiten.
2. **ASM separat:** lokale HTTP-Freigabe-/Export-Demo verifiziert; eine Discovery-Übergabe evaluieren.
3. **PXAPI bedingt:** Codebelege vorhanden, Runtime-Demo blockiert; zunächst Service-/Pilotlogik statt VC-SaaS behaupten.

Keine verifizierten Kunden, Umsätze, ROI-Daten oder komplette integrierte DYAI-Plattform. Keine externe Nachricht versendet, kein Formular abgeschickt. Die Recherche wurde zunächst außerhalb des öffentlichen Repositories erstellt. Auf ausdrücklichen Nutzerwunsch sind die Ergebnisdokumente und technischen Protokolle jetzt hier veröffentlicht; Source-Clones und Dependencies bleiben außerhalb.

## Lieferumfang A–G
| Teil | Datei | Inhalt |
|---|---|---|
| A/B | `02_Decision_and_Readiness.md` | Executive Memo unter 800 Wörtern, Readiness, sechs Thesen, Tests, Wettbewerb, IP/Budget/Kapazität, Audit |
| C | `03_Investor_Shortlist.md` | 15 Kandidaten mit Quellen, Personen, Kontaktweg, Score und Qualifikationslücken |
| D | `04_Partner_Matrix.md` | 10 Partner; klare Trennung von Pilot, Design-, strategischer und Kanalpartnerschaft |
| E | `05_Top5_Investor_Packs.md` | Top 5 nach Score: Crane, Fly, HTGF, UVC, Mätch; individuelle Drafts und Konfliktfragen |
| F | `06_Product_and_Marketing_Packs.md` | 3 One-Pager, 3-Minuten-Demos, EN/DE-Pitches, LinkedIn-/Investor-/Partnerentwürfe |
| G | `investor_register.csv/.json`, `partner_register.csv/.json` | Stabile IDs, Status, Quellen, Mapping und nächste Aktionen |
| Vorstufe | `01_FAST_PASS.md` | Ursprüngliche erste Auswahl; Update-Hinweis beachten, Deep Pass hat Vorrang |
| Nachweise | `evidence/` | Test-, Build-, HTTP-/CLI-Demo- und Fehlversuchsprotokolle |

`DYAI_Research_Report.md` bündelt die aktuellen Hauptdokumente. `DYAI_Research_Package.zip` enthält Bericht, Einzeldokumente, Register und kompakte Nachweise, **keine** Source-Clones, Dependencies oder echten Kundendaten.

## Nicht überinterpretieren
- 15 geprüfte Kandidaten sind nicht 15 vollständig qualifizierte Investoren; **alle B**, zwei ohne verifizierten Pitchweg. Sieben aktuelle datierte eigene Beteiligungen plus drei year-only Nachweise sind keine garantierte offene Allocation.
- Scores priorisieren ausschließlich die jeweilige zugeordnete Produktthese, nicht Investmentwahrscheinlichkeit. Kein vollständiges sechsfaches Scoring jedes Fonds. UNKNOWN gibt keine positiven Evidenzpunkte; veröffentlichte Tickets ohne DYAI-Budget ergeben keinen Ticket-Fit.
- 10 Partner haben nachvollziehbare fachliche Anknüpfungspunkte; namentliche Budgethalter und Kaufabsicht sind überwiegend UNKNOWN.
- Deutschland-/Europa-/US-Abdeckung ist stärker als Asien/Golf/Kanada/Australien. Keine abgeschlossene weltweite 30–50-Fonds-Due-Diligence behauptet.
- Confluence-Inhalte und drei wichtige Repositories waren nicht zugänglich. Genehmigte Produktabsicht, Gesellschaft und exklusive Verwertungsrechte bleiben offen.
- Zwei lokale Demo-Pfade, **keine LIVE_DEMO_VERIFIED**, kein selbst verifizierter Live-KI-Workflow.

## Jetzt tun – Empfehlungen, nicht ausgeführte Aktionen
1. Absender/Gesellschaft, IP-Rechte und verfügbare Founder-Zeit belegen; Claims intern freigeben.
2. Synthetische Plumbline-/ASM-Demos anhand Protokollen reproduzieren; PXAPI-Laufzeit in geeigneter Umgebung herstellen.
3. Einen Pilot fokussieren: inovex → iteratec → Netlight; nur ein Produkt je Gespräch.
4. Investor-Fit qualifizieren: Fly → HTGF → Mätch → UVC → Crane; bei Crane vorher Konfliktprüfung.
5. Kontaktstatus erst nach tatsächlicher menschlicher Aktion ändern. Keine automatische Mail-/LinkedIn-Sequenz.


---

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


---

# Worldwide Investor Shortlist – 15 geprüfte Kandidaten, keine 15 fertigen Leads
Stand 11.10.2026 · PARTIAL_EVIDENCE · alle NOT_CONTACTED
Die Scores gelten ausschließlich für das zugeordnete Produkt. Alle B: offene Gesellschafts-, Team-, IP- oder Marktfragen verhindern eine vollständige Qualifikation. UNKNOWN ist kein Ausschluss; dokumentierte Ausschlüsse würden dagegen unabhängig vom Score gelten. Keine fiktiven E-Mails.
## Scoring
Missing evidence gets 0. Stage max requires stage + pre-revenue + sole/small team evidence; 12 for stage, 15 for stage + pre-product/inception, remainder only if explicit. Geography 15 explicit Europe/global or demonstrated German investment, 8 indirect evidence. Activity 15 dated own investment in 2025/26, 10 year-only investment; no points for portfolio news, applications or fund launch alone. Ticket points only for evidenced support when DYAI budget not known; published ticket does not establish fit. Contact 10 published email/application, 8 contact form, 6 official social profile; 0 absent. Strategic and product points are analyst judgments grounded in cited thesis. All B because company, team and/or commercial qualification unresolved.

|Rang|Investor|Produkt|Score|Kontakt|
|---|---|---|---:|---|
|1|Crane Venture Partners|Plumbline|81|https://crane.vc/contact/|
|2|Fly Ventures|Plumbline|80|mailto:gabriel@fly.vc|
|3|HTGF|Plumbline|77|https://www.htgf.de/en/contact/|
|4|UVC Partners|Plumbline|74|mailto:pitch@uvcpartners.com|
|5|Mätch VC|Plumbline|74|https://airtable.com/appUy59AKXgdug59f/shrl8ZrqEdEQmvBdn|
|6|firstminute capital|ASM|73|https://form.typeform.com/to/pCFphSxu|
|7|Seedcamp|ASM|64|https://seedcamp.typeform.com/to/pMlqt8|
|8|Antler Continental Europe|ASM|62|https://www.antler.co/apply|
|9|boldstart ventures|Plumbline|61|https://boldstart.vc/contact-us/|
|10|Entourage|ASM|61|https://www.linkedin.com/in/pieterjanbouten/|
|11|Playfair|ASM|60|https://playfair.vc/pitch-us.php|
|12|Angular Ventures|Plumbline|60|https://angularventures.com/contact|
|13|Point Nine|ASM|59|UNKNOWN|
|14|Tiny Supercomputer Investment Company|ASM|55|mailto:hello@tiny.vc|
|15|Lunar Ventures|Plumbline|50|UNKNOWN|

## 1. Crane Venture Partners · INV-CRANE
- **Land:** UK / global offices
- **Website:** https://crane.vc/
- **Produkt:** Plumbline
- **These / spezifischer Fit (Analystenbewertung):** Foundational technology from inception; relevant recent code-change security investment, with important conflict caveat.
- **Phase:** Inception through Seed
- **Ticket:** UNKNOWN
- **Jüngste belegte Aktivität:** Led Hacktron USD2.9m pre-seed; total round, not Crane ticket
- **Ereignisdatum / belegte Genauigkeit:** 2026-05-13
- **Publikationsdatum:** 2026-05-13
- **Ansprechperson:** Scott Sage
- **Geografie:** Global founders; Europe supported on partner biographies
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** SUPPORTED_INFERENCE: inception investing; explicit revenue rule UNKNOWN
- **Kontakt / Apply:** https://crane.vc/contact/
- **Konfliktprüfung:** Laminar, Ona and Hacktron: direct/adjacent agent and software-quality overlap
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Ask conflict-routing permission before confidential details. Separate evidence adequacy from vulnerability discovery.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Scott, we are exploring Plumbline at DYAI. Foundational technology from inception; relevant recent code-change security investment, with important conflict caveat. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 81 = 24 + 15 + 15 + 15 + 0 + 8 + 4 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://crane.vc/ (Abruf 2026-10-11; Publikation UNKNOWN); https://crane.vc/team (Abruf 2026-10-11; Publikation UNKNOWN); https://crane.vc/contact/ (Abruf 2026-10-11; Publikation UNKNOWN); https://www.globenewswire.com/news-release/2026/05/13/3294234/0/en/hacktron-raises-2-9m-pre-seed-to-bring-ai-powered-security-testing-to-every-code-change.html (Abruf 2026-10-11; Publikation 2026-05-13)

## 2. Fly Ventures · INV-FLY
- **Land:** Germany / Europe
- **Website:** https://fly.vc/
- **Produkt:** Plumbline
- **These / spezifischer Fit (Analystenbewertung):** First-check European technical-founder mandate fits a narrow executable reliability layer better than a broad agent suite.
- **Phase:** First check / zero to one
- **Ticket:** UNKNOWN
- **Jüngste belegte Aktivität:** Zymtrace seed follow-on explicitly confirmed by company
- **Ereignisdatum / belegte Genauigkeit:** 2026-03-11
- **Publikationsdatum:** 2026-03-11
- **Ansprechperson:** Gabriel Matuschka
- **Geografie:** Technical founders across Europe expressly stated
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** UNKNOWN
- **Kontakt / Apply:** mailto:gabriel@fly.vc
- **Konfliktprüfung:** GitButler (developer workflow); zymtrace (runtime infrastructure) adjacency
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Demonstrate requirement/evidence mismatch, disclose open-source base, ask whether workflow-layer defensibility meets fund bar.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Gabriel, we are exploring Plumbline at DYAI. First-check European technical-founder mandate fits a narrow executable reliability layer better than a broad agent suite. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 80 = 24 + 12 + 15 + 15 + 0 + 10 + 4 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://fly.vc/ (Abruf 2026-10-11; Publikation UNKNOWN); https://fly.vc/team (Abruf 2026-10-11; Publikation UNKNOWN); https://zymtrace.com/article/zymtrace-funding/ (Abruf 2026-10-11; Publikation 2026-03-11)

## 3. HTGF · INV-HTGF
- **Land:** Germany
- **Website:** https://www.htgf.de/en/
- **Produkt:** Plumbline
- **These / spezifischer Fit (Analystenbewertung):** Official Digital Tech thesis explicitly includes developer tools and SDLC infrastructure.
- **Phase:** Pre-seed / Seed
- **Ticket:** UNKNOWN
- **Jüngste belegte Aktivität:** kausable seed follow-on explicitly named; round total EUR12m, HTGF share UNKNOWN
- **Ereignisdatum / belegte Genauigkeit:** 2026-07-23
- **Publikationsdatum:** 2026-07-23
- **Ansprechperson:** Axel Nitsch
- **Geografie:** Germany evidenced through domestic investing; entity-specific eligibility UNKNOWN
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** UNKNOWN
- **Kontakt / Apply:** https://www.htgf.de/en/contact/
- **Konfliktprüfung:** AI infrastructure adjacency; full current conflict review incomplete
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Confirm entity age, German operating requirements, solo-founder fit and minimum technical moat; then share Plumbline CLI demo.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Axel, we are exploring Plumbline at DYAI. Official Digital Tech thesis explicitly includes developer tools and SDLC infrastructure. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 77 = 23 + 12 + 15 + 15 + 0 + 8 + 4 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://www.htgf.de/en/digital-tech/ (Abruf 2026-10-11; Publikation UNKNOWN); https://www.htgf.de/en/team/axel-nitsch-2/ (Abruf 2026-10-11; Publikation UNKNOWN); https://www.htgf.de/en/kausable-seed-round/ (Abruf 2026-10-11; Publikation 2026-07-23)

## 4. UVC Partners · INV-UVC
- **Land:** Germany
- **Website:** https://www.uvcpartners.com/
- **Produkt:** Plumbline
- **These / spezifischer Fit (Analystenbewertung):** European B2B and AI mandate plus enterprise network; meaningful technical moat is a qualification hurdle.
- **Phase:** Early to Growth; seed demonstrated
- **Ticket:** UNKNOWN: first-cheque amount not sufficiently supported in retained evidence
- **Jüngste belegte Aktivität:** kausable seed co-lead explicitly named
- **Ereignisdatum / belegte Genauigkeit:** 2026-07-23
- **Publikationsdatum:** 2026-07-23
- **Ansprechperson:** Andreas Unseld
- **Geografie:** European B2B founders; German kausable investment
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** UNKNOWN
- **Kontakt / Apply:** mailto:pitch@uvcpartners.com
- **Konfliktprüfung:** Cirql One business context; Aleph Alpha enterprise AI adjacency
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Show reproducible comparison and clarify pre-revenue minimum before full deck.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Andreas, we are exploring Plumbline at DYAI. European B2B and AI mandate plus enterprise network; meaningful technical moat is a qualification hurdle. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 74 = 20 + 10 + 15 + 15 + 0 + 10 + 4 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://www.uvcpartners.com/ (Abruf 2026-10-11; Publikation UNKNOWN); https://www.uvcpartners.com/contact (Abruf 2026-10-11; Publikation UNKNOWN); https://www.htgf.de/en/kausable-seed-round/ (Abruf 2026-10-11; Publikation 2026-07-23)

## 5. Mätch VC · INV-MAETCH
- **Land:** Germany
- **Website:** https://www.maetch.vc/
- **Produkt:** Plumbline
- **These / spezifischer Fit (Analystenbewertung):** Highly technical B2B teams plus Mittelstand access could support evidence-gate pilots in engineering organizations.
- **Phase:** Early / Pre-seed
- **Ticket:** UNKNOWN
- **Jüngste belegte Aktivität:** kausable seed follow-on explicitly named
- **Ereignisdatum / belegte Genauigkeit:** 2026-07-23
- **Publikationsdatum:** 2026-07-23
- **Ansprechperson:** Daniel Dilger
- **Geografie:** Europe expressly targeted
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** UNKNOWN
- **Kontakt / Apply:** https://airtable.com/appUy59AKXgdug59f/shrl8ZrqEdEQmvBdn
- **Konfliktprüfung:** Blockbrain enterprise knowledge; LILY infrastructure adjacency
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Test relevance to industrial software teams; confirm solo/team requirement and fund cheque before pitch.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Daniel, we are exploring Plumbline at DYAI. Highly technical B2B teams plus Mittelstand access could support evidence-gate pilots in engineering organizations. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket. Daniel Dilger identified by official contact link; partner title not verified in fetched slice.
- **Score:** 74 = 20 + 12 + 15 + 15 + 0 + 8 + 4 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://www.maetch.vc/ (Abruf 2026-10-11; Publikation UNKNOWN); https://www.htgf.de/en/kausable-seed-round/ (Abruf 2026-10-11; Publikation 2026-07-23)

## 6. firstminute capital · INV-FIRSTMINUTE
- **Land:** UK
- **Website:** https://www.firstminute.capital/
- **Produkt:** ASM
- **These / spezifischer Fit (Analystenbewertung):** European inception investing with AI and developer-tools portfolio makes human-approved product context relevant.
- **Phase:** Inception; no stage too early
- **Ticket:** GBP1m–3m published; DYAI round need UNKNOWN
- **Jüngste belegte Aktivität:** Neno prior round co-led in 2025, disclosed 25 Aug 2026; 2026 follow-on participation NOT established
- **Ereignisdatum / belegte Genauigkeit:** 2025
- **Publikationsdatum:** 2026-08-25
- **Ansprechperson:** Michael Stothard
- **Geografie:** European founders explicitly targeted
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** SUPPORTED_INFERENCE: inception; explicit revenue rule UNKNOWN
- **Kontakt / Apply:** https://form.typeform.com/to/pCFphSxu
- **Konfliktprüfung:** Tessl direct/adjacent AI-native development; n8n workflow platform
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Conflict check on Tessl first; explain canonical file and approval semantics, not a competing code generator.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Michael, we are exploring ASM at DYAI. European inception investing with AI and developer-tools portfolio makes human-approved product context relevant. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 73 = 21 + 15 + 15 + 10 + 0 + 8 + 4 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://www.firstminute.capital/ (Abruf 2026-10-11; Publikation UNKNOWN); https://www.firstminute.capital/team (Abruf 2026-10-11; Publikation UNKNOWN); https://www.firstminute.capital/news-announcements/firstminute-backs-neno-rebuilding-accounting-for-europe-s-smes (Abruf 2026-10-11; Publikation 2026-08-25)

## 7. Seedcamp · INV-SEEDCAMP
- **Land:** UK
- **Website:** https://seedcamp.com/
- **Produkt:** ASM
- **These / spezifischer Fit (Analystenbewertung):** Structured context and verifiable evidence provide a specific bridge to Topograph thesis, not proof of direct PM-sector mandate.
- **Phase:** Seed evidenced; pre-seed case also listed on official news
- **Ticket:** UNKNOWN
- **Jüngste belegte Aktivität:** Led Topograph EUR2m seed; source identifies Sia and evidence-grounded infrastructure thesis
- **Ereignisdatum / belegte Genauigkeit:** 2026-03-20
- **Publikationsdatum:** 2026-03-20
- **Ansprechperson:** Sia Houchangnia
- **Geografie:** European investing evidenced historically; legal Germany eligibility UNKNOWN
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** UNKNOWN
- **Kontakt / Apply:** https://seedcamp.typeform.com/to/pMlqt8
- **Konfliktprüfung:** Dust and Flow Engineering adjacency; full PM portfolio check incomplete
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Confirm earliest stage and Germany route; show ASM approval/export rather than claiming agent autonomy.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Sia, we are exploring ASM at DYAI. Structured context and verifiable evidence provide a specific bridge to Topograph thesis, not proof of direct PM-sector mandate. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 64 = 18 + 12 + 8 + 15 + 0 + 8 + 3 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://seedcamp.com/ (Abruf 2026-10-11; Publikation UNKNOWN); https://seedcamp.com/contact/ (Abruf 2026-10-11; Publikation UNKNOWN); https://seedcamp.com/views/seedcamp-leads-topographs-e2m-seed-to-fix-the-broken-infrastructure-behind-global-kyb/ (Abruf 2026-10-11; Publikation 2026-03-20)

## 8. Antler Continental Europe · INV-ANTLER
- **Land:** Global / Germany route
- **Website:** https://www.antler.co/continental-europe
- **Produkt:** ASM
- **These / spezifischer Fit (Analystenbewertung):** Co-founder matching can address an actual team-capacity gap; only relevant if residency is feasible.
- **Phase:** Inception / residency
- **Ticket:** Up to EUR500k first commitment; conditional, not guaranteed
- **Jüngste belegte Aktivität:** Accepting applications currently; dated 2025/26 investment UNKNOWN in reviewed source
- **Ereignisdatum / belegte Genauigkeit:** UNKNOWN
- **Publikationsdatum:** UNKNOWN
- **Ansprechperson:** Christoph Klink
- **Geografie:** Berlin/Amsterdam residency and Continental Europe route
- **Solo-Founder:** YES for entry/matching; solo investment eligibility UNKNOWN
- **Vorumsatz:** SUPPORTED_INFERENCE: inception / co-founder formation
- **Kontakt / Apply:** https://www.antler.co/apply
- **Konfliktprüfung:** LangWatch overlaps Plumbline; other portfolio conflicts UNKNOWN
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Confirm existing-project admission, full-time residency, current economics and whether sole founder may receive investment.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Christoph, we are exploring ASM at DYAI. Co-founder matching can address an actual team-capacity gap; only relevant if residency is feasible. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 62 = 14 + 15 + 15 + 0 + 4 + 10 + 4 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://www.antler.co/continental-europe (Abruf 2026-10-11; Publikation UNKNOWN); https://www.antler.co/apply (Abruf 2026-10-11; Publikation UNKNOWN)

## 9. boldstart ventures · INV-BOLDSTART
- **Land:** USA
- **Website:** https://boldstart.vc/
- **Produkt:** Plumbline
- **These / spezifischer Fit (Analystenbewertung):** Explicit technical-founder, AI infra and agents mandate; geographical and portfolio conflicts prevent qualification.
- **Phase:** Inception, before incorporation allowed in thesis
- **Ticket:** USD500k–15m published; not inferred from portfolio rounds
- **Jüngste belegte Aktivität:** Keycard backed since 2025 on official portfolio; exact transaction date UNKNOWN
- **Ereignisdatum / belegte Genauigkeit:** 2025
- **Publikationsdatum:** UNKNOWN
- **Ansprechperson:** Ellen Chisa
- **Geografie:** UNKNOWN: German entity acceptance
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** SUPPORTED_INFERENCE: pre-company investing
- **Kontakt / Apply:** https://boldstart.vc/contact-us/
- **Konfliktprüfung:** Tessl, Snyk agent governance, Keycard: substantial overlap
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Ask whether a German entity and evidence-gate layer can be considered alongside Tessl/Snyk.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Ellen, we are exploring Plumbline at DYAI. Explicit technical-founder, AI infra and agents mandate; geographical and portfolio conflicts prevent qualification. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 61 = 24 + 15 + 0 + 10 + 0 + 8 + 4 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://boldstart.vc/ (Abruf 2026-10-11; Publikation UNKNOWN); https://boldstart.vc/contact-us/ (Abruf 2026-10-11; Publikation UNKNOWN)

## 10. Entourage · INV-ENTOURAGE
- **Land:** Belgium
- **Website:** https://www.entourage.io/
- **Produkt:** ASM
- **These / spezifischer Fit (Analystenbewertung):** Operator-led early enterprise/AI investing could help productization, but stated traction preference is a current weakness.
- **Phase:** Pre-seed / Seed; initial traction prioritized
- **Ticket:** UNKNOWN
- **Jüngste belegte Aktivität:** kausable seed co-lead explicitly named
- **Ereignisdatum / belegte Genauigkeit:** 2026-07-23
- **Publikationsdatum:** 2026-07-23
- **Ansprechperson:** Pieterjan Bouten
- **Geografie:** German kausable investment evidenced
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** UNKNOWN; initial traction explicitly prioritized
- **Kontakt / Apply:** https://www.linkedin.com/in/pieterjanbouten/
- **Konfliktprüfung:** Conveo AI research and Aikido developer security adjacency
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Obtain real pilot/user evidence first; initial traction is not yet evidenced for DYAI.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Pieterjan, we are exploring ASM at DYAI. Operator-led early enterprise/AI investing could help productization, but stated traction preference is a current weakness. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 61 = 16 + 6 + 15 + 15 + 0 + 6 + 3 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://www.entourage.io/ (Abruf 2026-10-11; Publikation UNKNOWN); https://www.htgf.de/en/kausable-seed-round/ (Abruf 2026-10-11; Publikation 2026-07-23)

## 11. Playfair · INV-PLAYFAIR
- **Land:** UK
- **Website:** https://playfair.vc/
- **Produkt:** ASM
- **These / spezifischer Fit (Analystenbewertung):** Pre-revenue acceptance and open pitch process suit a small, early ASM product-discovery hypothesis.
- **Phase:** Pre-seed
- **Ticket:** UNKNOWN; round-size definitions are not cheque sizes
- **Jüngste belegte Aktivität:** Wassist investment verified; 2026 only in search excerpt, not rendered page: exact current transaction date UNKNOWN
- **Ereignisdatum / belegte Genauigkeit:** UNKNOWN
- **Publikationsdatum:** UNKNOWN
- **Ansprechperson:** Chris Smith
- **Geografie:** UK focus, invests across Europe explicitly
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** YES: pre-revenue and sometimes pre-product explicit
- **Kontakt / Apply:** https://playfair.vc/pitch-us.php
- **Konfliktprüfung:** StackOne governance adjacency; conflicting ecommerce exclusion vs Wassist portfolio
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Qualify current cheque and solo policy; explicitly ask about thesis/portfolio inconsistency if relevant. Do not pitch PXAPI as MarTech.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Chris, we are exploring ASM at DYAI. Pre-revenue acceptance and open pitch process suit a small, early ASM product-discovery hypothesis. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket. Published thesis excludes AdTech/MarTech and Ecommerce, while Wassist is labeled Ecommerce. Treat as source conflict, not a relaxed blanket mandate.
- **Score:** 60 = 17 + 15 + 15 + 0 + 0 + 10 + 3 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://playfair.vc/thesis.php (Abruf 2026-10-11; Publikation UNKNOWN); https://playfair.vc/team.php (Abruf 2026-10-11; Publikation UNKNOWN); https://playfair.vc/companies/wassist (Abruf 2026-10-11; Publikation UNKNOWN)

## 12. Angular Ventures · INV-ANGULAR
- **Land:** UK / Israel
- **Website:** https://angularventures.com/
- **Produkt:** Plumbline
- **These / spezifischer Fit (Analystenbewertung):** Inception-stage technical-founder mandate in Europe matches product stage; hard-tech bar may exceed workflow moat.
- **Phase:** Inception
- **Ticket:** UNKNOWN
- **Jüngste belegte Aktivität:** UNKNOWN: current dated deal not verified
- **Ereignisdatum / belegte Genauigkeit:** UNKNOWN
- **Publikationsdatum:** UNKNOWN
- **Ansprechperson:** Gil Dibner
- **Geografie:** Europe and Israel explicitly
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** SUPPORTED_INFERENCE: inception; explicit revenue rule UNKNOWN
- **Kontakt / Apply:** https://angularventures.com/contact
- **Konfliktprüfung:** UNKNOWN: full portfolio not reviewed
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Verify current deployment, ticket and tolerance for workflow-layer rather than novel deep technology.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Gil, we are exploring Plumbline at DYAI. Inception-stage technical-founder mandate in Europe matches product stage; hard-tech bar may exceed workflow moat. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 60 = 20 + 15 + 15 + 0 + 0 + 8 + 2 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://angularventures.com/ (Abruf 2026-10-11; Publikation UNKNOWN); https://angularventures.com/team (Abruf 2026-10-11; Publikation UNKNOWN); https://angularventures.com/contact (Abruf 2026-10-11; Publikation UNKNOWN)

## 13. Point Nine · INV-P9
- **Land:** Europe / Germany-associated
- **Website:** https://www.pointnine.com/
- **Produkt:** ASM
- **These / spezifischer Fit (Analystenbewertung):** Early AI/B2B investing with explicit recent pre-seed entries; ASM needs a stronger moat and adoption case.
- **Phase:** Early stage; explicit 2026 pre-seed portfolio
- **Ticket:** USD1m–10m per company; not explicitly first cheque
- **Jüngste belegte Aktivität:** F13, grubel and Forithmus listed as 2026 pre-seed; exact closing dates UNKNOWN
- **Ereignisdatum / belegte Genauigkeit:** 2026
- **Publikationsdatum:** UNKNOWN
- **Ansprechperson:** Louis Coppey
- **Geografie:** Global investing stated; Berlin F13 pre-seed listed
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** UNKNOWN
- **Kontakt / Apply:** UNKNOWN
- **Konfliktprüfung:** Poolside and Anthropic software-development/platform adjacency
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Find valid official pitch path; /contact is 404. Confirm ticket interpretation and PM thesis.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Louis, we are exploring ASM at DYAI. Early AI/B2B investing with explicit recent pre-seed entries; ASM needs a stronger moat and adoption case. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 59 = 19 + 12 + 15 + 10 + 0 + 0 + 3 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://www.pointnine.com/ (Abruf 2026-10-11; Publikation UNKNOWN)

## 14. Tiny Supercomputer Investment Company · INV-TINY
- **Land:** UK / Germany
- **Website:** https://tiny.vc/
- **Produkt:** ASM
- **These / spezifischer Fit (Analystenbewertung):** Early European checks and explicit non-lead model could suit a focused ASM syndicate after a pilot.
- **Phase:** Pre-seed / Seed
- **Ticket:** 200–250K stated; currency UNKNOWN
- **Jüngste belegte Aktivität:** UNKNOWN: dated 2025/26 investment not primary-verified
- **Ereignisdatum / belegte Genauigkeit:** UNKNOWN
- **Publikationsdatum:** UNKNOWN
- **Ansprechperson:** Philipp Moehring
- **Geografie:** Mostly European startups explicitly stated
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** UNKNOWN
- **Kontakt / Apply:** mailto:hello@tiny.vc
- **Konfliktprüfung:** UNKNOWN: current complete portfolio not reviewed
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Confirm currency, recent deployment, solo acceptance, and lead-investor dependency. Avoid mismatched Andy/Ophelia profile links on page.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Philipp, we are exploring ASM at DYAI. Early European checks and explicit non-lead model could suit a focused ASM syndicate after a pilot. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 55 = 15 + 12 + 15 + 0 + 0 + 10 + 3 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://tiny.vc/ (Abruf 2026-10-11; Publikation UNKNOWN)

## 15. Lunar Ventures · INV-LUNAR
- **Land:** Germany
- **Website:** https://www.lunar.vc/
- **Produkt:** Plumbline
- **These / spezifischer Fit (Analystenbewertung):** Technical founder backing and CTO/scientist team are relevant, but missing official pitch route stops outreach.
- **Phase:** Day zero / Pre-seed
- **Ticket:** UNKNOWN primary-verified; secondary report EUR750k–1m not treated as confirmed
- **Jüngste belegte Aktivität:** Fund II announced May 2025 in secondary reporting; dated primary deal UNKNOWN
- **Ereignisdatum / belegte Genauigkeit:** UNKNOWN
- **Publikationsdatum:** UNKNOWN
- **Ansprechperson:** Mick Halsband
- **Geografie:** European portfolio evidenced; mandate detail UNKNOWN
- **Solo-Founder:** UNKNOWN
- **Vorumsatz:** SUPPORTED_INFERENCE: day zero
- **Kontakt / Apply:** UNKNOWN
- **Konfliktprüfung:** Wasp, deepset, Otera adjacency
- **Qualifikation:** B – QUALIFICATION_NEEDED
- **Confidence zur gesamten Qualifikation:** MEDIUM
- **Nächste Aktion:** Find official pitch route; /contact and /imprint returned 404. Do not guess email.
- **Individueller Gesprächseinstieg (Entwurf):** Hello Mick, we are exploring Plumbline at DYAI. Technical founder backing and CTO/scientist team are relevant, but missing official pitch route stops outreach. Would you review a non-confidential technical brief and help us qualify fit before a fundraising discussion?
- **Grenzen:** Score is prioritization, not investment probability. A recent round is not proof of an open allocation today. Round total is not investor ticket.
- **Score:** 50 = 23 + 15 + 8 + 0 + 0 + 0 + 4 (Produkt / Phase / Geo / Aktivität / Ticket oder Support / Kontakt / Zusatznutzen).
- **Quellen:** https://www.lunar.vc/ (Abruf 2026-10-11; Publikation UNKNOWN); https://www.lunar.vc/team (Abruf 2026-10-11; Publikation UNKNOWN); https://www.lunar.vc/portfolio (Abruf 2026-10-11; Publikation UNKNOWN)

---

# D. Strategic & Paid Design Partner Matrix
**11.10.2026 · PARTIAL_EVIDENCE · alle NOT_CONTACTED**

Die offiziellen Leistungsseiten belegen Kompetenzen, nicht Bedarf oder Kaufabsicht. Rollen sind **Käuferhypothesen**, keine verifizierten Budgethalter. Kein bestehender Kunde oder warmer Kontakt wird behauptet. Preis, Umfang und Datenschutz erst gemeinsam vereinbaren. Ein Kanalmodell folgt erst nach nachgewiesener Wiederholbarkeit; keine sofortige Reseller-Partnerschaft unterstellen.

| ID / Priorität | Organisation / Region | Produkt / Transaktion | Konkreter Vorschlag und Käuferrolle | Originalquelle / offizieller Kontakt | Risiko / nächster Schritt |
|---|---|---|---|---|---|
| PAR-INOVEX / 1 | inovex / Deutschland | Plumbline / **PAID_PILOT** | Ein agentisch bearbeitetes, nicht vertrauliches Engineering-Arbeitspaket mit bestehendem Review vergleichen. AI-/Engineering-Practice-Leitung, tatsächlicher Budgethalter UNKNOWN | [AI / Agentic Coding](https://www.inovex.de/de/leistungen/artificial-intelligence/); [Kontakt](https://www.inovex.de/de/kontakt/), Jürgen Budnick als Routingkontakt, nicht bestätigter Einkäufer | Eigenentwicklung möglich. Nach zuständigem Delivery-Owner fragen; nur synthetische Demo senden |
| PAR-ITERATEC / 2 | iteratec / Deutschland | ASM / **DESIGN_PARTNERSHIP** | Eine Discovery-to-Delivery-Übergabe in kanonischer Datei evaluieren; Bezahlung separat vereinbaren. Product-/Delivery-Leitung UNKNOWN | [Leistungen](https://www.iteratec.com/de/); [Kontakt](https://www.iteratec.com/de/kontakt), office@iteratec.com | Neues Tool darf Workshops nicht verlangsamen. Einen bestehenden, anonymisierbaren Ablauf auswählen |
| PAR-NETLIGHT / 3 | Netlight / Europa | ASM / **PAID_PILOT** | Product-/Engineering-Übergabe mit Ziel-/Bedürfnis-Rückverfolgbarkeit. Engagement Lead / Product Practice UNKNOWN | [Product, Engineering, AI](https://www.netlight.com/); [Business-Kontakt](https://www.netlight.com/contact) | Kein bewiesener Bedarf. Qualifizieren, ob Übergabeprobleme überhaupt teuer genug sind |
| PAR-CODECENTRIC / 4 | codecentric / Deutschland | Plumbline / **PAID_PILOT** | Evidence-Gate ergänzend zu AI-Coding evaluieren. AI-/Engineering-Practice UNKNOWN | [AI-Coding/Hermes-Angebot](https://www.codecentric.de/); [Kontakt](https://www.codecentric.de/kontakt) | Eigenes Angebot kann konkurrieren. Vor vertraulichen Details Ergänzung statt Ersatz klären |
| PAR-MAYFLOWER / 5 | Mayflower / Deutschland | Plumbline / **DESIGN_PARTNERSHIP** | Einen nicht vertraulichen Agent-Workflow gegen explizite Evidenzregeln testen. mAIstack-/Engineering-Verantwortliche UNKNOWN | [mAIstack / Agenten](https://mayflower.de/); [Kontaktbereich](https://mayflower.de/#contact) | Eigener Stack und On-Prem-Kompetenz; Buy-vs-build. Interesse an schmalem Gate statt Plattformwechsel prüfen |
| PAR-VALTECH / 6, bedingt | Valtech / international | PXAPI / **PAID_PILOT** | Ein autorisierter statischer Homepage-Audit mit nachvollziehbarer Belegkette. Experience-/Commerce-Leitung UNKNOWN | [Angebot](https://www.valtech.com/offerings/); [Kontakt](https://www.valtech.com/contact/) | **DEMO_BLOCKER** Python-Laufzeit; Konkurrenz zu bestehendem Audit-Stack. Erst nach echter Ausführung anbieten |
| PAR-ADESSO / 7 | adesso / Europa | Plumbline / **STRATEGIC_PARTNERSHIP** | Nicht vertrauliche Evaluation nachvollziehbarer AI-Delivery-Prüfung. AI-/Software-Engineering-Unit UNKNOWN | [KI-Angebot](https://www.adesso.de/de/impulse/kuenstliche-intelligenz/index.jsp); [Kontakt](https://www.adesso.de/de/kontakt/index.jsp) | Enterprise-Einkauf kann zu früh sein. Erst technisches Routing, keine unterstellte Einkaufsfreigabe |
| PAR-DICONIUM / 8 | diconium / international | PXAPI / **DESIGN_PARTNERSHIP**, später ggf. **CHANNEL_PARTNERSHIP** | Evidenzgebundene Website-Diagnose in einen Digital-Commerce-Workflow einpassen. Commerce-/Data-Leitung UNKNOWN | [Angebot](https://diconium.com/en/); [Kontakt](https://diconium.com/en/contact-us/) | Laufzeitblocker und bestehende Tools. Kanalmodell erst nach bezahlter, wiederholbarer Nutzung prüfen |
| PAR-DEPT / 9 | DEPT / international | ASM / **DESIGN_PARTNERSHIP** | Explizite menschliche Freigabe von Produktkontext neben vorhandener Orchestrierung evaluieren. AI-/Product-Leitung UNKNOWN | [DEPTIFY / Agent-Angebot](https://www.dept.global/); [Kontakt](https://www.dept.global/contact-us/), berlin@dept.global | Eigene Orchestrierung = Wettbewerbsnähe. Kein vertrauliches Plattformkonzept senden, bevor Abgrenzung geklärt |
| PAR-THOUGHTWORKS / 10, zurückgestellt | Thoughtworks / international | Plumbline / **STRATEGIC_PARTNERSHIP** | Vergleichende Evaluation gegen eigene Delivery-Governance, nicht generischer Sales-Pitch. AI-/Engineering-Leitung UNKNOWN | [AI/works, Agent/works](https://www.thoughtworks.com/en-de/what-we-do/ai); [Kontakt](https://www.thoughtworks.com/en-de/contact-us) | Starke Überschneidung. Extrahiertes Formular meldet „Marketo Form ID is invalid“; Browserroute SOURCE_NEEDED. Keine HR-Adresse als Ersatz |

**Quellenstatus:** Alle URLs am 11.10.2026 gelesen; Publikationsdaten der Leistungs-/Kontaktseiten UNKNOWN. Kontaktwege nicht abgesendet, Zustellung nicht getestet. Confidence: MEDIUM für Leistungs-/Kontaktzuordnung, LOW für individuellen Bedarf und Budget. Alle Partner **B – QUALIFICATION_NEEDED**; Thoughtworks zusätzlich Kontaktweg-Blocker, PXAPI-Kandidaten Demo-Blocker.

## Abnahme und Zahlungsbeweis
- Plumbline: vorhandenes Review als Baseline; unsupported completion claims, Fehlalarme und zusätzlicher Reviewaufwand zählen. Positive Fixture und negative Fixture reichen zum Erklären, nicht zum ROI-Nachweis.
- ASM: ein freigegebenes Artefakt; unabhängiger Reviewer rekonstruiert Ziel, Persona und Akzeptanzkriterien. Ausgangsprozess dokumentieren; keine willkürliche Prozentverbesserung versprechen.
- PXAPI: jeder Befund muss auf Messung derselben Ausführung zurückführen; nicht messbar bleibt unbekannt. Käufer bewertet Verifikationsaufwand und Nutzbarkeit, nicht vermeintlichen Conversion-Effekt.
- Bezahlter Pilot = vereinbarter Leistungsumfang, Preis, Ergebnis und tatsächlicher Vertrag/Zahlung. Ein Design-Partner-Gespräch ist noch kein Umsatz.

## Kapazitätsregel – Empfehlung, keine bekannte Teamplanung
Zunächst höchstens **einen** Pilot gleichzeitig verpflichtend zusagen, solange verfügbare Teamstunden UNKNOWN sind. Verantwortlichen, feste Liefergrenze und Abbruchkriterium festlegen. Ein Pilot endet auch mit „kein ausreichender Nutzen“; das ist verwertbare Evidenz und kein Anlass, Wirkungszahlen zu erfinden.


---

# E. Fünf individualisierte Investor-Pakete
**11.10.2026 · DRAFT_ONLY · NOT_CONTACTED · B – QUALIFICATION_NEEDED**

Top 5 nach konservativem Score der zugeordneten These: Crane 81, Fly 80, HTGF 77, UVC 74, Mätch 74. Damit sind alle fünf Plumbline-bezogen. Dies ist **keine** ausgewogene Produktquote; ASM folgt mit firstminute und Seedcamp im Register. Die Versandfolge weicht aus Konfliktgründen ab: **Fly → HTGF → Mätch → UVC → Crane**. Gesellschafts-/IP-/Absenderfreigabe zuerst; Fundraisingbedarf noch UNKNOWN. Partner-/Dealquellen und Komponenten stehen ausführlich in `03_Investor_Shortlist.md`.

## 1. Crane — Scott Sage — INV-CRANE
**Warum individuell:** Inception-/Softwareinfrastruktur-Fokus und [Hacktron-Lead vom 13.05.2026](https://www.globenewswire.com/news-release/2026/05/13/3294234/0/en/hacktron-raises-2-9m-pre-seed-to-bring-ai-powered-security-testing-to-every-code-change.html). Die Runde von $2,9 Mio. ist nicht Cranes Ticket. **Kontakt:** [offizielles Formular](https://crane.vc/contact/); [Team](https://crane.vc/team).

**Angle:** Nachweisadäquanz einer Erledigungsbehauptung, nicht Security-Scanning. **Konfliktprüfung:** Hacktron, Laminar, Ona. Bei möglicher Überschneidung erst nicht vertrauliche Einordnung, dann entschiedenes Go/No-Go.

**Subject:** A narrow evidence gate for agentic delivery — conflict check first

> Hello Scott, Crane’s investment in Hacktron makes your view on software-quality infrastructure especially relevant. We are evaluating Plumbline, an early-stage requirement-to-evidence gate for agentic delivery. A locally executed CLI demo rejects an inadequate synthetic evidence case and accepts a matching integration fixture. It does not establish universal semantic correctness or customer ROI. Before sharing more, could you confirm whether this workflow is too close to Hacktron, Laminar or Ona? If not, we would value a short fit discussion about the technical and commercial proof you would require from an early German/EU company.

**Anlage:** Plumbline-One-Pager, positives/negatives CLI-Ergebnis, Lizenzhinweis. Kein vollständiges internes Architekturpaket.
**Erwarteter Einwand:** „Warum keine Funktion bestehender Evals?“ Antwort: Die konkrete Nachweisregel vorführen; Differenzierung als zu prüfende Hypothese, nicht Behauptung. **Qualifizierungsfragen:** aktueller Deal-Appetit, Rechtsform-/Geografievorgaben, Solo-/Pre-Revenue-Akzeptanz, Konflikt-Routing, erforderliche Moat-Belege.

## 2. Fly — Gabriel Matuschka — INV-FLY
**Warum individuell:** [Fly](https://fly.vc/) adressiert technische Gründer in Europa vom ersten Check an; [Zymtrace](https://zymtrace.com/article/zymtrace-funding/) bestätigt Flys Follow-on am 11.03.2026. **Kontakt:** gabriel@fly.vc, veröffentlicht im [Teamprofil](https://fly.vc/team).

**Angle:** Eine messbare Engineering-Prüfung statt breiter Agentenplattform. **Konfliktprüfung:** GitButler und Zymtrace als benachbarte Workflows; kein automatischer Ausschluss.

**Subject:** Plumbline: testing evidence adequacy in agentic software delivery

> Hello Gabriel, Fly’s first-check focus on European technical founders is why I am approaching you with a deliberately narrow product. Plumbline checks whether declared completion evidence meets explicit delivery requirements. We have locally verified its deterministic gate with positive and negative synthetic fixtures; there is no customer ROI claim yet. Your continued backing of Zymtrace suggests relevant infrastructure experience, although our workflow is different. Would you review a short technical brief and help us qualify whether this can become a defensible product rather than an open-source feature? Our next commercial proof is a bounded, paid engineering evaluation.

**Anlage:** Drei-Minuten-Demo, bestehende Review-Baseline als noch auszufüllender Pilotplan. **Einwand:** „Workflow, kein Deep Tech.“ Antwort: Nicht technische Tiefe erfinden; Käuferproblem, Integrationskosten und wiederholbaren Nutzen zeigen. **Fragen:** gewünschte Mindestvalidierung; aktuelle Phase/Ticket; Founder-Kapazität; Open-Source-Geschäftsmodell.

## 3. HTGF — Axel Nitsch — INV-HTGF
**Warum individuell:** [Digital-Tech-These](https://www.htgf.de/en/digital-tech/) umfasst Devtools/SDLC-Infrastruktur; [Axel Nitsch](https://www.htgf.de/en/team/axel-nitsch-2/) ist passender fachlicher Ansprechpartner. [kausable 23.07.2026](https://www.htgf.de/en/kausable-seed-round/) war für HTGF ein **Follow-on**, nicht Lead. **Kontakt:** [offizieller Kontakt](https://www.htgf.de/en/contact/).

**Angle:** Nachvollziehbare Entwicklungsprüfung, potenziell für deutsche B2B-Engineering-Teams. **Eligibility:** Unternehmensalter, Standortanforderungen und konkrete Gesellschaft noch zu prüfen; nicht automatisch zulässig.

**Subject:** Plumbline — prüfbarer Evidenz-Gate für agentische Softwareentwicklung

> Guten Tag Herr Nitsch, Ihre Digital-Tech-These nennt Developer Tools und SDLC-Infrastruktur. Dazu möchten wir Plumbline fachlich einordnen lassen: einen frühen, ausführbaren Gate, der deklarierte Nachweise gegen explizite Anforderungen prüft. Lokal wurden 77 Assertions sowie ein positiver und negativer synthetischer CLI-Fall ausgeführt. Das belegt den engen Prüfpfad, nicht Kundenwirkung oder vollständige semantische Korrektheit. Nächster Schritt ist eine begrenzte, bezahlte Engineering-Evaluation. Können wir vor einem ausführlichen Pitch Gesellschafts-/Phasen-Fit und die von Ihnen erwartete technische Differenzierung klären? Einen nicht vertraulichen One-Pager mit den Grenzen der Demo stellen wir gern bereit.

**Anlage:** Deutsche Kurzfassung, IP-/Contributor-Status mit UNKNOWN statt pauschalem Eigentumsclaim. **Einwand:** „Wer besitzt welche Rechte?“ Antwort erst mit Nachweisen, nicht GitHub-Owner. **Fragen:** Gründungsalter/DE-Betrieb, Vorumsatz-/Solo-Fit, Ticket, Rechte-/Finanzierungsunterlagen.

## 4. UVC — Andreas Unseld — INV-UVC
**Warum individuell:** B2B-/AI-Portfolio auf [offizieller Seite](https://www.uvcpartners.com/); [kausable-Co-Lead](https://www.htgf.de/en/kausable-seed-round/) vom 23.07.2026 belegt eigene jüngste Seed-Aktivität. **Kontakt:** pitch@uvcpartners.com, [Kontaktquelle](https://www.uvcpartners.com/contact). Person vor Versand erneut auf aktuelle Zuständigkeit prüfen.

**Angle:** Engineering-Nachweis als enger Einstieg, nicht „Enterprise AI Platform“. **Konflikte:** Cirql One/Aleph Alpha als benachbarte Kontexte. **Hürde:** Frühester kommerzieller Reifegrad und substanzielle Differenzierung offen.

**Subject:** Qualifying an evidence-gate product before an enterprise-AI pitch

> Hello Andreas, UVC’s B2B focus and co-lead of kausable’s July seed round prompted this fit check. Plumbline is an early reliability layer for agentic software delivery: its locally verified CLI checks whether supplied evidence satisfies explicit requirements. We are not presenting an integrated agent platform, production deployment or proven ROI. The immediate milestone is one paid comparison against an engineering team’s existing review process. Is a pre-revenue project at this level within your current scope, and what defensibility evidence would you require before a fuller discussion? We would start with a non-confidential brief and portfolio-overlap check.

**Anlage:** Messplan mit Fehlalarm-/Reviewkosten, nicht unvalidierte Savings-Folie. **Einwand:** „Zu früh / zu wenig technische Tiefe.“ Konsequenz: zurückstellen, keine künstliche Traktion erfinden. **Fragen:** früheste Phase, zuständiger Partner, Ticket, Pilotbeweis, IP-Anforderungen.

## 5. Mätch VC — Daniel Dilger — INV-MAETCH
**Warum individuell:** [Offizielle These](https://www.maetch.vc/) zu technischen Teams und Unternehmensnetzwerk; [kausable-Follow-on](https://www.htgf.de/en/kausable-seed-round/) 23.07.2026. Daniel Dilger ist über den offiziellen Kontakt verlinkt; exakter Partnertitel nicht verifiziert. **Startup-Kontakt:** [offizielles Airtable-Formular](https://airtable.com/appUy59AKXgdug59f/shrl8ZrqEdEQmvBdn). **Nicht** `hi@maetch.vc` verwenden: auf der Seite für Investoren ausgewiesen.

**Angle:** Industrielle Softwareteams als zu prüfende Design-Partner-Gruppe, nicht vorhandene Kundenpipeline. **Konflikte:** Blockbrain/LILY; die LBBW-Blockbrain-News nicht als Mätch-Neuinvestment zählen.

**Subject:** Plumbline: prüfbare Nachweise für agentisch erstellte Software

> Hallo Daniel, Mätchs Ausrichtung auf technische B2B-Teams macht Ihre Perspektive für Plumbline interessant. Wir prüfen einen schmalen Produktkern: Passen die gelieferten Nachweise zu einer behaupteten erledigten Anforderung? Ein lokaler CLI-Test zeigt sowohl Ablehnung ungeeigneter Evidenz als auch Annahme einer passenden synthetischen Integrations-Fixture. Daraus leiten wir noch keine Kundenwirkung ab. Zunächst suchen wir eine begrenzte, bezahlte Engineering-Evaluation. Passt diese frühe Phase grundsätzlich zu Mätch, und könnte die Fragestellung für Softwareteams in Ihrem Unternehmensumfeld relevant sein? Vor vertraulichen Details würden wir Portfolioüberschneidungen und Gesellschafts-/Team-Fit klären.

**Anlage:** Nicht vertraulicher One-Pager + ein klares Pilot-Abnahmekriterium. **Einwand:** „Beratungsprojekt statt Produkt.“ Antwort: standardisierbare Prüfung als Hypothese; nach dem Pilot wiederkehrenden Bedarf untersuchen. **Fragen:** Solo-/Teamregel, Erstticket, aktuelle Phase, technische Zuständigkeit, konkretes Intro nur nach bestätigtem Interesse.

## Versandkontrolle
Keine Nachricht versendet. Absender und Gesellschaft müssen wahrheitsgemäß ergänzt werden. Nach Gespräch Score/Status mit Datum aktualisieren; keine Antwort ist kein Desinteressebeweis. Kein automatisiertes Nachfassen, keine Kontaktanreicherung und kein vertraulicher Anhang vor Konfliktprüfung. Englischsprachige Texte behaupten keine gesicherte deutsche Rechtsform; die tatsächliche Entität ist vor Versand zu konkretisieren.


---

# F. Drei Produkt-, Demo- und Marketing-Pakete
**11.10.2026 · Entwürfe, nicht veröffentlicht · keine Kunden-/Umsatzbehauptungen**

Quellen: eingefrorene Commits und Ausführungslogs in `02_Decision_and_Readiness.md`. Alle wirtschaftlichen Vorteile sind zu prüfende Hypothesen. Jeder Pitch unten umfasst weniger als 100 Wörter. Demo-Skripte beschreiben den engen überprüften Kern; bei PXAPI sind sie ausdrücklich ein **noch nicht ausgeführter Plan**.

# 1. Plumbline — One-Pager
**Headline:** Passing tests are not the whole story.
**Subline:** Check whether completion evidence meets explicit delivery requirements.

**Problemhypothese:** Agentisch erzeugte Software kann als fertig gemeldet werden, obwohl Nachweise eine relevante Anforderung nicht abdecken. **Käufer:** Engineering-/Platform-Leitung; spezifischer Budgethalter noch unbekannt.

**Produkt heute:** Repository-nahe Integrity-Prüfungen; lokal verifizierter deterministischer CLI-Kern mit positiver und negativer synthetischer Fixture. 77 Assertions bestanden. Ein optionaler Evidence-Manifest-Pfad ist kein universell aktives Sicherheitsnetz; ohne Manifest kann der betreffende Check passieren. Tokens/Dateireferenzen beweisen nicht automatisch tatsächliche Wirkung. Keine verifizierte Integration mit Agent Team oder ASM.

**Angebot:** Ein bezahlter, begrenzter Vergleich mit dem vorhandenen Reviewprozess. Ergebnis: Bericht über erkannte Nachweislücken, Fehlalarme, zusätzlichen Reviewaufwand und nicht abgedeckte Fälle. Nicht: fehlerfreie Software oder garantierte Einsparung.

**Differenzierungshypothese:** Eine explizite Anforderung-Nachweis-Regel direkt im Entwicklungsablauf. Gegen Braintrust, LangSmith und manuelles Review validieren. **Geschäftsmodellhypothese:** bezahlte Evaluation → wiederkehrende Team-/Repository-Nutzung mit Support. Preis und Zahlungsbereitschaft UNKNOWN.

**IP:** MIT-/claude-flow-Anteile sichtbar; vollständige Contributor-/Gesellschaftsrechte UNKNOWN. **Investment-Meilenstein:** unabhängiger Workflowvergleich plus mindestens ein belastbarer bezahlter Nutzungsfall, nicht weitere Repositories.

### Drei-Minuten-Demo
- **0:00–0:30:** Eine synthetische Anforderung und ihre geforderte Nachweisart zeigen. „Diese Fixture, keine Kundendaten.“
- **0:30–1:15:** `fake-only` über das CLI ausführen: Exit 3; präzise erklären, weshalb die Evidenzregel nicht erfüllt ist.
- **1:15–2:00:** Passende Integrations-Fixture: Exit 0. Nicht suggerieren, dass ein anderes reales System damit getestet wurde.
- **2:00–2:30:** Regel und Eingabedatei nebeneinander lesen; zeigen, was das Gate tatsächlich prüft und was nicht.
- **2:30–3:00:** Pilotfrage: Erkennt die Regel relevante Lücken besser als das bestehende Review, ohne unvertretbare Fehlalarme?

**Notwendige technische Maßnahmen (maximal drei):** Für diesen CLI-Kern keine Codeänderung erforderlich. **DEMO_BLOCKER:** keiner für den belegten Fixture-Pfad; reproduzierbare Umgebung und identische Inputs beibehalten. **MARKETING_BLOCKER:** manuelle Aktivierung/Opt-in und semantische Grenzen sichtbar machen. **RELEASE_BLOCKER:** Integrations-/Sicherheitsprüfung für reale Kundenumgebung. **DEFERRED:** vollständige autonome Delivery-Plattform.

### EN pitch
Plumbline is an early reliability framework for agentic software delivery. Its locally verified CLI checks whether supplied evidence satisfies explicit requirements. A passing test alone is not treated as proof of every intended outcome. We are seeking engineering teams for a paid evaluation on one bounded workflow, measuring missed evidence, false positives and review cost against their existing process. This is a narrow deterministic gate, not a guarantee of semantic correctness or an integrated autonomous development platform.

### DE pitch
Plumbline prüft, ob die vorgelegten Nachweise zu expliziten Anforderungen passen. Der enge CLI-Kern wurde lokal mit positiven und negativen synthetischen Fällen verifiziert. Wir suchen Engineering-Teams für eine begrenzte, bezahlte Evaluation gegenüber ihrem bisherigen Reviewprozess. Gemessen werden Nachweislücken, Fehlalarme und zusätzlicher Prüfaufwand. Noch nicht belegt sind Kundenwirkung, wiederkehrender Umsatz oder eine vollständige autonome Entwicklungsplattform. Unser Angebot ist ein überprüfbarer Einstieg, keine Garantie fehlerfreier Software.

### LinkedIn-Entwurf
Grüne Tests beantworten nicht automatisch jede Produktanforderung. Mit Plumbline untersuchen wir einen engen Ansatz: explizite Anforderungen an die Nachweise hinter einer Erledigungsbehauptung. Lokal funktionieren ein positiver und ein negativer synthetischer CLI-Fall. Noch offen ist der wirtschaftliche Nutzen im echten Reviewprozess. Wir suchen ein Engineering-Team für einen klar abgegrenzten Vergleich – einschließlich Fehlalarmen und zusätzlichem Aufwand. Keine autonome Plattform, kein garantierter ROI. Welche Nachweise fehlen euch heute am häufigsten bei AI-generierten Änderungen?

### Individueller Investor-Entwurf
An Gabriel Matuschka / Fly: „Your first-check focus on European technical founders is relevant to our deliberately narrow Plumbline evaluation. Could we qualify what evidence would distinguish a defensible reliability product from a feature? We can show a locally verified gate, but have not established customer ROI.“ Vollständiger Text und belegter Kontakt in Paket E.

### Separater Design-Partner-Entwurf — inovex
**Betreff:** Begrenzte Evaluation von Nachweisregeln im Agentic-Coding-Workflow

> Guten Tag, Ihr Agentic-Coding-Angebot ist der Anlass für eine konkrete Evaluationsfrage: Könnte ein expliziter Nachweis-Gate Ihre bestehenden Reviews sinnvoll ergänzen? Plumbline hat einen lokal verifizierten CLI-Kern; Kundenwirkung behaupten wir nicht. Wir schlagen einen bezahlten, eng begrenzten Vergleich auf einem freigegebenen Arbeitspaket vor. Bewertet würden Nachweislücken, Fehlalarme und Reviewaufwand. Wer verantwortet bei Ihnen solche Engineering-Evaluationen? Zunächst würden wir nur eine synthetische Demo zeigen, ohne Zugriff auf Kundencode.

# 2. ASM — One-Pager
**Headline:** Make product intent explicit before agents build.
**Subline:** A canonical product file, structured story mapping and human approval.

**Problemhypothese:** Ziele, Personas, Bedürfnisse und Entscheidungen gehen zwischen Discovery und Engineering verloren. **Käufer:** Head of Product, Product Ops oder Delivery-Leitung.

**Produkt heute:** Strukturiertes kanonisches Modell, Referenzvalidierung, explizite Freigabe, YAML-Persistenz und Export. 706 Tests bestanden. HTTP-Lesen, Freigeben, Exportieren und Ablehnung unbekannter Personas lokal verifiziert. Die lokale Seite lieferte HTML; eine echte Browser-End-to-End-Nutzung und reale Modellqualität wurden nicht überprüft. Keine automatische integrierte Umsetzung in Software behaupten.

**Angebot:** Eine Discovery-to-Engineering-Übergabe begleiten. Ergebnis: freigegebene Produktdatei und Vergleich, ob ein unabhängiger Reviewer Ziel, Persona, Anforderungen und offene Fragen korrekt rekonstruieren kann. **Nutzenhypothese:** weniger Kontextverlust; keine behauptete prozentuale Zeitersparnis.

**Wettbewerb:** Miro AI, Productboard und bestehende Dokument-/Workshop-Prozesse. Unterschied als Hypothese: kontrollierbare, portable Datei mit expliziten Referenzen und Freigabe. **Geschäftsmodell:** zunächst Design-Partnerschaft; später Team-/Workspace-Lizenz nur bei nachgewiesener wiederkehrender Nutzung. **IP:** fehlende Root-LICENSE und Rechtekette vor externer Verteilung klären.

### Drei-Minuten-Demo
- **0:00–0:30:** Kopierte öffentliche Produkt-Fixture zeigen; klar sagen: keine echten Kundendaten, kein aktiver KI-Provider.
- **0:30–1:15:** Kanonisches Modell per HTTP lesen, Beziehung von Ziel/Persona/Need/Story am tatsächlichen JSON erklären.
- **1:15–2:00:** Explizite synthetische Freigabe auslösen, Status lesen, YAML exportieren. Synthetischer Approver ist kein Authentifizierungsnachweis.
- **2:00–2:30:** Ein Modell mit gültig formatierter, aber unbekannter Persona einreichen; 422 `unknown_persona` zeigen. Syntaxfehler nicht mit Referenzvalidierung verwechseln.
- **2:30–3:00:** Export und Grenzen erklären: maschinenlesbarer Produktkontext, noch kein autonomer Discovery-/Delivery-Kreislauf.

**Notwendige technische Maßnahmen (maximal drei):** Keine Codeänderung für den belegten HTTP-Pfad. Für eine ausdrücklich interaktive Browser-Demo zuerst deren Bedienpfad separat testen; dies ist eine Verifikation, kein geforderter Vollausbau. **DEMO_BLOCKER:** nur für Live-KI-Claims fehlt ein realer Provider-/Outputnachweis. **MARKETING_BLOCKER:** lokale HTTP-Verifikation nicht als Browser-/Live-KI-Erfolg darstellen. **RELEASE_BLOCKER:** echte Authentifizierung, Zugriffsschutz und Mandantengrenzen vor Kundendaten. **DEFERRED:** Jira-Bidirektionalität, Multiplayer und Agent-Delivery-Integration.

### EN pitch
ASM is an early story-mapping tool built around a canonical, agent-readable product file. It connects goals, personas, needs and explicit human approval. Its tests pass locally, and we verified the read, approve and export workflow through HTTP. Live AI quality and customer outcomes remain unverified. We are seeking a product team to evaluate one discovery-to-engineering handoff: can a reviewer recover the original intent and identify missing requirements more reliably? The immediate offer is a scoped design partnership, not an autonomous product team.

### DE pitch
ASM hält Ziele, Personas, Bedürfnisse und Stories in einer kanonischen Produktdatei zusammen. Explizite menschliche Freigabe und Referenzvalidierung sind Teil des bestehenden Codes; Lesen, Freigeben und Export wurden lokal per HTTP verifiziert. Wir suchen ein Produktteam für eine abgegrenzte Discovery-to-Engineering-Übergabe. Der Test: Kann ein unabhängiger Reviewer die ursprüngliche Absicht und fehlende Anforderungen besser erkennen? Live-KI-Qualität und Kundenwirkung sind noch offen. ASM ist heute kein autonomes Produktteam und keine fertige Enterprise-Collaboration-Suite.

### LinkedIn-Entwurf
Der schwierigste Teil einer Übergabe ist oft nicht das Dokument, sondern die verlorene Absicht. ASM untersucht einen kleinen Gegenentwurf: strukturierte Produktziele, Personas, Bedürfnisse und Stories in einer kanonischen Datei – mit expliziter menschlicher Freigabe. Der lokale HTTP-Kern ist verifiziert; Live-KI-Qualität und wirtschaftlicher Nutzen sind es noch nicht. Wir suchen ein Produktteam für genau eine Übergabe als Design-Partnerschaft. Nicht „mehr KI“, sondern eine prüfbare Frage: Versteht die nächste Person, warum etwas gebaut werden soll?

### Individueller Investor-Entwurf — Seedcamp / Sia Houchangnia
**Subject:** Human-approved product context — an early ASM fit check

> Hello Sia, Seedcamp’s Topograph investment drew our attention to your interest in structured, evidence-grounded infrastructure. ASM addresses a different problem: preserving product intent in a canonical, human-approved file. We verified reading, approval and export locally through HTTP, but have not established customer outcomes or live AI quality. Would you help us qualify whether this early product-context thesis fits Seedcamp? Our next milestone is one measured discovery-to-engineering handoff, not a claim of autonomous delivery.

Route: [Seedcamp-Pitchformular](https://seedcamp.typeform.com/to/pMlqt8). Bezug: [Topograph-Mitteilung 20.03.2026](https://seedcamp.com/views/seedcamp-leads-topographs-e2m-seed-to-fix-the-broken-infrastructure-behind-global-kyb/). Kein direkter PM-Mandatsbeweis.

### Separater Design-Partner-Entwurf — iteratec
**Betreff:** Eine Discovery-Übergabe mit freigegebener Produktdatei evaluieren

> Guten Tag, für Ihre Product-/Delivery-Arbeit möchten wir einen begrenzten Design-Partner-Test vorschlagen. ASM hält Produktkontext in einer strukturierten Datei; Freigabe und Export sind lokal verifiziert. Könnten wir an einer anonymisierbaren Übergabe prüfen, ob ein unabhängiger Reviewer die ursprünglichen Ziele und Anforderungen nachvollziehen kann? Scope, Abnahme und eine mögliche Vergütung würden wir vorab vereinbaren. Es geht nicht um einen Plattformwechsel oder um autonome Discovery. Wer wäre bei Ihnen für diese Problemstellung zuständig?

# 3. PXAPI — One-Pager
**Headline:** A finding should come with its evidence.
**Subline:** Static website diagnosis that keeps failed measurements separate from observed issues.

**Problemhypothese:** Agenturen verbringen Zeit damit, automatisierte Befunde zu verifizieren und ihren Kunden verständlich zu belegen. **Käufer:** Digital-/SEO-/Experience-Agentur, Website-Verantwortliche.

**Produkt heute:** Code für statische Homepage-Analyse und eine Finding→Evidence→Measurement-Kette. Unknown, absent und not-applicable sind nicht austauschbar. Findings benötigen bekannte Evidenz derselben Ausführung. **CODE_EVIDENCE_ONLY**: Tests und End-to-End-Ausführung in dieser Umgebung nicht durchgeführt. Python ≥3.13 fehlt; Interpreter-Download scheiterte an TLS. Keine fertige Pixelkiez-Oberfläche, kein deployter Diagnose-Agent aus separatem Repo abgeleitet.

**Bedingtes Angebot:** Nach erfolgreicher Laufzeitprüfung ein begrenzter, autorisierter Homepage-Audit mit nachvollziehbarem Bericht. **Nicht verkaufen:** laufende Produktions-API, garantierte Such-/KI-Sichtbarkeit, Conversion-Steigerung oder umfassende Rechts-/Accessibility-Konformität.

**Alternativen:** Screaming Frog, Lighthouse, manuelle Agenturprüfung. **Differenzierungshypothese:** explizite Belegbarkeit und Unknown-Semantik reduzieren Nachprüfung. **Geschäftsmodellentscheidung:** zunächst technologiegestützter Service; Lizenz/API erst bei standardisierten wiederkehrenden Aufträgen. **VC-Fit:** derzeit schwächer als bei Plumbline/ASM. Rechtekette trotz MIT UNKNOWN.

### Drei-Minuten-Demo — PLAN, noch nicht ausgeführt
- **0:00–0:30:** Scope erläutern: eine autorisierte statische Homepage, kein vollständiger Website-Crawl.
- **0:30–1:15:** Analyse mit kompatibler Laufzeit starten. Nur tatsächlichen Output zeigen; bei Fehler abbrechen und Fehler benennen.
- **1:15–2:00:** Einen tatsächlich erzeugten Befund bis zur Messung derselben Ausführung zurückverfolgen. Keine Muster-JSON als Laufzeitoutput ausgeben.
- **2:00–2:30:** Kontrollierten Messfehler prüfen: Ergebnis unbekannt, nicht automatisch Website-Mangel. Dies ist erst nach Ausführung als verifiziert zu bezeichnen.
- **2:30–3:00:** Agentur-Reviewer bewertet Nutzbarkeit und Nachprüfaufwand. Keine Wirkungs-/Umsatzfolie.

**Notwendige technische Maßnahmen (zwei):** (1) kompatible Python-Laufzeit sicher bereitstellen; keine TLS-Prüfung abschalten. (2) Dependencies/Tests und einen autorisierten Positiv-/Fehlerfall ausführen und protokollieren. **DEMO_BLOCKER:** beide Schritte offen. **MARKETING_BLOCKER:** CODE_EVIDENCE_ONLY sichtbar lassen. **RELEASE_BLOCKER:** Eingabe-/Netzwerkschutz, Datenschutz und Betriebsverantwortung vor öffentlichem API-Betrieb prüfen. **DEFERRED:** JS-Rendering, komplette Website-Crawls, Billing und Multi-Tenant-SaaS, sofern nicht Pilotanforderung.

### EN pitch
PXAPI is an early website-analysis engine that links findings to evidence and measurements. Its code distinguishes an observed issue from a failed measurement, so a timeout should not become a negative verdict about a business. We are seeking an agency partner for a bounded evaluation of static-page diagnosis. A compatible runtime is still needed before the local demo can be verified. We make no production or conversion-impact claim. The commercial question is whether evidence-backed reports reduce manual verification enough to support repeatable paid delivery.

### DE pitch
PXAPI verknüpft Website-Befunde mit Evidenz und Messungen. Der Code trennt beobachtete Probleme von fehlgeschlagenen Messungen: Ein Timeout darf nicht automatisch zum negativen Unternehmensurteil werden. Wir suchen eine Agentur für eine begrenzte Evaluation statischer Homepage-Diagnosen. Die lokale Laufzeitprüfung steht noch aus; eine fertige Produktions-API oder Conversion-Wirkung behaupten wir nicht. Zunächst soll sich zeigen, ob die nachvollziehbaren Berichte manuelle Nachprüfung verringern und wiederholbare bezahlte Aufträge ermöglichen.

### LinkedIn-Entwurf
„Nicht messbar“ ist nicht dasselbe wie „schlecht“. PXAPI untersucht diese Unterscheidung in der Website-Diagnose: Befunde sollen auf Evidenz und konkrete Messungen zurückführen. Der Code ist geprüft, die lokale Ausführung wegen einer Laufzeitabhängigkeit noch nicht verifiziert. Wir suchen eine Agentur, die nach dieser Prüfung einen begrenzten Diagnosefall mit uns bewertet. Die Frage ist nicht, ob ein weiterer Scan möglich ist, sondern ob belegbare Ergebnisse die manuelle Nachprüfung tatsächlich erleichtern. Kein versprochener SEO- oder Conversion-Uplift.

### Individueller Investor-Entwurf — Tiny / Philipp Moehring, bewusst zurückgestellt
**Subject:** Service-first website diagnostics — qualifying whether equity is appropriate

> Hello Philipp, Tiny’s European pre-seed focus makes your perspective relevant to a financing question, not a ready fundraising claim. PXAPI links static website findings to their measurements. The code is reviewed, but local execution and paid demand remain unverified. We currently see a service-first evaluation rather than a proven venture-scale API. After a paid agency pilot, would this fit your scope, or would customer-funded development be more appropriate? We would not propose an equity round before clarifying repeatability and capital need.

Kontakt: hello@tiny.vc laut [offizieller Seite](https://tiny.vc/). **Nicht priorisiert:** Register-Tiny-Score gilt ASM, nicht PXAPI. Dieses Anschreiben ist bewusst nur ein späterer, individuell adressierter Qualifikationsentwurf; kein belegter PXAPI-Investor-Fit.

### Separater Design-Partner-Entwurf — Valtech, erst nach Runtime-Nachweis
**Betreff:** Nachvollziehbare Homepage-Befunde in einem begrenzten Agentur-Pilot

> Guten Tag, für Ihre Experience-/Commerce-Arbeit möchten wir einen kleinen Vergleich vorschlagen: Sind Website-Befunde leichter nutzbar, wenn jede Aussage bis zur konkreten Messung nachvollziehbar ist? PXAPI implementiert diese Evidenzkette für statische Homepage-Diagnosen. Derzeit fehlt uns noch der lokale Laufzeitnachweis; erst danach würden wir einen bezahlten Pilot anbieten. Wäre die Problemstellung für Ihre Audit-Verantwortlichen grundsätzlich relevant? Keine Conversion-Versprechen, kein vollständiger Website-Crawl und kein Zugriff auf Kundensysteme ohne ausdrückliche Freigabe.

# Gemeinsame Go-/No-Go-Regel
Ein Pitch darf vor Prüfung Interesse qualifizieren, aber keine nicht verifizierte Lieferung zusagen. Eine Pilotzusage benötigt Scope, Rechte, Verantwortliche, verfügbare Kapazität und Abnahmekriterien. Ein Investment-Pitch benötigt zusätzlich rechtliche Entität, vollständige Rechtekette und belastbaren Mittelverwendungsplan. Für keines der drei Angebote liegt unabhängiger Kunden-/Umsatzbeweis vor.
