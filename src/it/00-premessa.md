# Guida Pratica a Claude Code CLI

> **Versione 4.23 — maggio 2026** — verificata su Claude Code v2.1.123
> Licenza [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> ← [Prefazione](00-prefazione.md) | [Index](README.md) | [1. Cos'è Claude Code](01-cosè-claude-code.md) →

---

## Premessa

*Una guida pensata per chi vuole iniziare a usare Claude Code in modo professionale.*

Questa guida è un'introduzione pratica a **Claude Code**, la CLI agentica di Anthropic che porta il modello Claude direttamente nel terminale come collaboratore operativo, capace di leggere codice, eseguire comandi, modificare file e gestire workflow completi.

Il documento è pensato per **sviluppatori che vogliono iniziare a usare Claude Code in modo professionale**, senza affidarsi al passaparola o a tutorial frammentati. Trovi qui il percorso completo dall'installazione ai workflow avanzati, con esempi concreti tratti da scenari WordPress/PHP e progetti generici Node/TypeScript.

### Perché questa guida

Negli ultimi mesi mi sono passati davanti agli occhi parecchi contenuti su Claude Code, e a un certo punto ho riconosciuto due categorie ricorrenti.

La prima sono i **video tutorial** che ti spiegano cos'è lo strumento e si fermano lì. Utili nei primi dieci minuti, poi ti accorgi di aver guardato un trailer: hai visto cosa Claude Code può fare in astratto, ma non sai ancora come usarlo davvero su un tuo progetto.

La seconda sono le **guide a scambio email**: il post sui social *"ho preparato la guida definitiva, lasciami un commento e te la mando"*, il classico funnel commento → DM → landing page → form → newsletter (con spam annessi). A volte il PDF in fondo al funnel è anche fatto bene, ma il prezzo da pagare in attenzione e privacy è sproporzionato rispetto al valore.

A un certo punto mi sono fermato e ho pensato una cosa abbastanza ovvia:

> *Sto usando ogni giorno uno strumento che serve esattamente a produrre lavori complessi in tempi brevi.*
> *Perché non lo uso per scrivere la guida fatta bene che mi sarebbe piaciuto leggere e che non ho trovato?*

Quello che hai sotto gli occhi è il risultato. Tutto verificato sulla documentazione ufficiale di Anthropic — zero flag inventati, zero skill fantasiose pescate da thread Reddit non controllati. Nessun DM da scrivere, nessuna email da lasciare, nessuna newsletter a cui iscriverti per riceverla. È un PDF rilasciato sotto licenza **Creative Commons BY-SA 4.0**: lo scarichi, lo leggi, lo stampi, lo passi ai colleghi se lo trovi utile.

Proprio perché è un documento aperto e vivo, le segnalazioni dei lettori sono parte del processo: trovi i contatti per errata corrige e suggerimenti nella sezione [Feedback ed errata corrige](#feedback-ed-errata-corrige) qui sotto, oppure puoi inquadrare il QR code in copertina per raggiungere la pagina ufficiale della guida.

### A chi si rivolge

- Sviluppatori web (PHP, JavaScript, Python) con familiarità con il terminale e Git
- Professionisti che vogliono integrare l'AI nel proprio workflow quotidiano in modo consapevole
- Team tecnici che stanno valutando l'adozione di strumenti AI agentici nei processi di sviluppo
- Partecipanti ai workshop Mavida su *vibe coding* (sviluppo guidato da prompt strutturati anziché scrittura manuale del codice) e AI-assisted development

### Cosa troverai

I primi sei capitoli coprono le basi: cosa fa Claude Code, come installarlo, come strutturare il primo progetto, i comandi essenziali, il Plan Mode e i principi di prompt engineering. I capitoli 7-14 approfondiscono i meccanismi che fanno la differenza tra un uso casuale e uno professionale: memoria persistente con `CLAUDE.md`, gestione del contesto, sicurezza, Skill, plugin, MCP, subagent e hook. I capitoli finali presentano workflow pratici, tips avanzati e una riflessione onesta su quando la CLI supera la chat e quando invece è meglio restare in browser.

### Cosa non troverai

Questa non è una reference esaustiva: per quello c'è la documentazione ufficiale (linkata nell'Allegato B). L'obiettivo è mettere il lettore in condizione di lavorare produttivamente in una o due giornate, sapendo dove approfondire quando serve. Non troverai nemmeno hype sulle capacità dell'AI: il tono è tecnico, onesto sui limiti e attento ai rischi reali (sicurezza, prompt injection, costi nascosti dei token).

### Come leggerla

Se sei alle prime armi, leggi in sequenza almeno fino al capitolo 7 (CLAUDE.md). Se invece hai già installato Claude Code e cerchi best practice specifiche, usa l'indice come riferimento tematico. In fondo trovi un glossario dei termini ricorrenti (Allegato A) e le fonti ufficiali per verifiche e approfondimenti (Allegato B).

### Come è stata scritta questa guida

Questa guida è meta-circolare: è stata scritta usando Claude Code stesso. Il sorgente è un file Markdown unico (`guida.md`); una pipeline di build in Python lo converte in due formati PDF — A4 per stampa ufficio, 17×24 cm per la versione libro — attraverso **Pandoc** e **WeasyPrint**, in un unico comando `python scripts/build_pdf.py`.

Ogni capitolo è stato discusso, scritto e affinato in sessioni di Claude Code, con il modello che rileggeva il documento intero per mantenere coerenza fra capitoli, controllava i riferimenti incrociati e aggiornava il `CHANGELOG.md` a ogni release. Quando una scelta editoriale richiedeva discussione — titolo, posizione di una sezione, tono di un passaggio — usavo Plan Mode per allinearci prima di toccare il file. Il versionamento ha seguito una semantica simile a SemVer (incrementi minor per nuovi capitoli o sezioni, patch per fix editoriali), tracciato puntualmente nel `CHANGELOG.md` del repository.

La parte umana resta tutta: l'idea iniziale, i tagli editoriali, la voce, la revisione finale, le decisioni di tono. Quello che Claude Code ha tolto è la fatica meccanica di tenere sincronizzato un documento in evoluzione su più dimensioni — contenuto, struttura, cross-reference, build — lasciandomi più tempo per quello che conta, cioè scrivere bene. È esattamente il tipo di workflow che questa guida descrive nel resto delle pagine.

### Feedback ed errata corrige

Questa guida è un documento vivo: nonostante la cura nella verifica, errori, imprecisioni od omissioni sono sempre possibili — e Claude Code stesso evolve rapidamente. **Se trovi un refuso, un esempio che non funziona, una procedura ormai obsoleta o un argomento che meriterebbe approfondimento, segnalalo.** Le segnalazioni verranno raccolte e integrate nelle prossime versioni, con riconoscimento ai contributori nelle note di rilascio.

Puoi inviare feedback scrivendo a **[maurizio@mavida.com](mailto:maurizio@mavida.com)** indicando, dove possibile, capitolo e sezione di riferimento. La pagina ufficiale della guida — con eventuali aggiornamenti, errata corrige e versioni successive — è raggiungibile su **[maurizio.mavida.com/guida-claude-code](https://maurizio.mavida.com/guida-claude-code/)** o tramite il QR code in copertina. Ogni segnalazione — anche minima — è benvenuta e contribuisce a migliorare il lavoro per chi leggerà la guida dopo di te.

---


---

> ← [Prefazione](00-prefazione.md) | [Index](README.md) | [1. Cos'è Claude Code](01-cosè-claude-code.md) →
