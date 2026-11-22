#!/usr/bin/env python3
"""Builds the Alerta homepage and changelog in PT, EN and DE.

    python3 Alerta/_src/build.py

Writes index.html, en.html, de.html, changelog.html, changelog-en.html and
changelog-de.html next to this folder. Edit the text here, never the generated
files. To add a release, put a new entry at the top of LOG.

Jekyll does not publish folders that start with "_", so this script stays
off the live site.
"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent

LANGS = ["pt", "en", "de"]
HOME = {"pt": "index.html", "en": "en.html", "de": "de.html"}
CHANGELOG = {"pt": "changelog.html", "en": "changelog-en.html", "de": "changelog-de.html"}

APP_STORE = "https://apps.apple.com/us/app/alerta/id6759662896"
PLAY = "https://play.google.com/store/apps/details?id=com.waltertengler.alerta"
CONTACT = "walter.tengler@gmail.com"

# Other apps listed in the footer (same list as before the redesign).
OTHER_APPS = [
    ("../Adsensemonitor/", "AdSense Monitor"), ("../Aichive/", "Aichive"), ("../AppleIIASCIIArt/", "1977"),
    ("../MissileTag/", "Missile Tag"), ("../Bitpast/", "BitPast"), ("../Bomba/", "Bomba"),
    ("../CertificadoEnergetico/", "Certificado Energético"), ("../Comboiotreck/", "Comboiotreck"),
    ("../Conquer-GS/", "Conquer GS"), ("../CyanHero/", "CyanHero"), ("../EUEnergyMonitor/", "EU Energy Monitor"),
    ("../EasyDup/", "EasyDup"), ("../ExifEasy/", "ExifEasy"), ("../FCPXClean/", "FCPX Clean"),
    ("../File Vortex/", "File Vortex"), ("../Fire/", "Fire"), ("../Flipside/", "Flipside"), ("../Fluvio/", "Fluvio"),
    ("../Fugiu/", "Fugiu!"), ("../MegaconvertGS/", "MegaconvertGS"), ("../Pibup/", "PIBUP"),
    ("../RetroBrowse/", "Retro Browse"), ("../RetroGraphicsConverter/", "Retro Graphics"),
    ("../RetroTube/", "Retro Tube"), ("../RetroTV/", "Retro TV"), ("../SOSIberico/", "SOS Ibérica"),
    ("../Cuida24/", "Cuida24"), ("../Scanora/", "Scanora"), ("../Screen2Store/", "Screen2Store"), ("../SlimPix/", "SlimPix"),
    ("../Sobrium/", "Sobrium"), ("../Terramoto/", "Terramoto"), ("../TileTown/", "TileTown"),
    ("../TileTown%202/", "TileTown 2"), ("../Wallys Manager/", "Wally's Manager"), ("../climaviva/", "Clima Viva"),
    ("../coresdoamor/", "Cores do Amor"), ("../emergengy-reminder/", "Emergency Reminder"),
    ("../GSRemap/", "GS Remap"), ("../GSCommander/", "GS Commander"), ("../GSLauncher/", "GSLauncher"),
    ("../Conquer3/", "Conquer 3: Sandstorm"), ("../EmuBuddy/", "EmuBuddy"), ("../Demos/", "IIgs Demos"),
    ("../Hyperhaul/", "Hyperhaul"), ("../GTApple/", "Grand Theft Apple"), ("../Terra%20Incognita/", "Terra Incognita"),
    ("../Gaivota/", "GAIVOTA"), ("../Theos/", "Theos"),
]

# ---------------------------------------------------------------------------
# Text. Values may contain HTML; they are inserted as written.
# ---------------------------------------------------------------------------
T = {
"pt": dict(
    title="Alerta - Ocorrências de Proteção Civil em Tempo Real",
    keywords="proteção civil, incêndios, acidentes, sismos, terramotos, IPMA, Portugal, alertas, emergência, bombeiros, ANEPC, fogos, reportes cidadãos, comunidade, iOS app, Android app",
    description="Acompanhe ocorrências de proteção civil e sismos em Portugal em tempo real. Receba alertas quando surgem novos eventos perto de si e reporte incidentes na sua zona.",
    nav_new="Novidades", nav_privacy="Privacidade", nav_support="Suporte",
    status="Dados oficiais da ANEPC e do IPMA",
    h1="Avisos de proteção civil para a sua zona, no seu telemóvel.",
    lede="Veja todas as ocorrências da ANEPC e os sismos do IPMA num mapa em tempo real. Quando surge algo novo perto de si, ou dos locais que lhe importam, a Alerta avisa-o de imediato.",
    meta="Gratuito · iPhone, iPad, Mac e Android · 8 idiomas",
    play_badge="https://play.google.com/intl/en_us/badges/static/images/badges/pt_badge_web_generic.png",
    play_alt="Disponível no Google Play", apple_alt="Descarregar na App Store",
    hero_alt="Mapa da Alerta com as ocorrências ativas em Portugal e uma notificação de alerta",
    step="Passo",
    steps=[
        ("Defina a sua área", "Um raio à volta de onde está, distritos inteiros, ou locais que escolher, como a casa dos seus pais."),
        ("Escolha o que quer saber", "Incêndios, acidentes, inundações, quedas de árvores, sismos acima de uma magnitude. Só o que lhe interessa."),
        ("Receba o aviso", "Uma notificação com o tipo de ocorrência, a distância a que está e o local exato."),
    ],
    app_h="O que encontra na app",
    app_intro="Tudo o que a proteção civil publica, organizado para ser lido depressa, mesmo num momento de stress.",
    pairs=[
        ("06-detail", "Detalhe de uma ocorrência com meios no terreno e cronologia", None,
         "Cada ocorrência, em detalhe",
         "<p>Onde é, desde quando, em que estado está e quantos meios estão no local.</p>"
         "<ul><li>Bombeiros, veículos e meios aéreos</li><li>Cronologia desde o despacho</li><li>Nível de gravidade e estado atual</li></ul>"),
        ("02-stats-summary", "Estatísticas nacionais de ocorrências e meios", None,
         "O país em números",
         "<p>Ocorrências ativas, operacionais, veículos e meios aéreos em todo o país, com gráficos de 24 horas, 30 dias ou um ano, e por distrito.</p>"),
        ("04-earthquakes", "Mapa e lista de sismos do IPMA", None,
         "Sismos",
         "<p>Dados oficiais do IPMA para o Continente, a Madeira e os Açores, e do USGS para o resto do mundo. Histórico de 24 horas, 7 ou 30 dias, e avisos só acima da magnitude que escolher.</p>"),
        ("07-new-report", "Ecrã para criar um reporte com tipo, localização e fotografia", "Comunidade",
         "Reporte o que vê",
         "<p>Árvore caída, estrada cortada, falta de luz: escolha o tipo, tire uma foto e envie. Os dados de localização da foto são removidos antes de publicar, e um operador revê cada reporte.</p>"
         "<p>Inicie sessão com Apple ou Google, ou reporte de forma anónima.</p>"),
        ("08-account-reports", "Conta com nível de reputação e lista de reportes", None,
         "De Civil a Mítico",
         "<p>Dez níveis de reputação. Cada reporte confirmado por um operador aumenta a sua confiança, e reportes inválidos baixam-na. Acompanhe os seus reportes e o progresso para o próximo nível.</p>"
         '<div class="levels"><span>Civil</span><span>…</span><span>Vigia</span><span>…</span><span>Mítico</span></div>'),
    ],
    more_h="Mais funcionalidades",
    more=[
        ("Círculo de Segurança", "Partilhe a sua posição com família e amigos, envie um SOS ou diga que está em segurança."),
        ("Meus Locais", "Receba alertas para outros sítios além de onde está, como a casa dos pais ou a casa de férias."),
        ("Alertas por zona", "Siga distritos inteiros ou comandos sub-regionais da ANEPC."),
        ("Grandes ocorrências", "Um aviso nacional quando uma ocorrência mobiliza muitos meios. Pode desativá-lo."),
        ("Alertas que o acompanham", "Opcional: a app atualiza a sua zona de alertas em segundo plano quando viaja, mesmo fechada."),
        ("Legenda do mapa", "Todas as cores e símbolos explicados, e um olho nas ocorrências em vigilância."),
    ],
    src_h="De onde vêm os dados",
    src_intro="Fontes públicas e oficiais, consultadas automaticamente.",
    sources=[
        ("ANEPC", "Autoridade Nacional de Emergência e Proteção Civil. Ocorrências em todo o território, verificadas a cada 10 minutos."),
        ("IPMA", "Instituto Português do Mar e da Atmosfera. Sismos no Continente, na Madeira e nos Açores."),
        ("USGS", "Serviço Geológico dos Estados Unidos. Sismos no resto do mundo."),
        ("Comunidade", "Reportes de utilizadores, moderados por operadores e sempre assinalados como tal."),
    ],
    notice="A Alerta é uma app informativa e não substitui os canais oficiais. Em caso de emergência, ligue <strong>112</strong>.",
    req_h="Requisitos",
    req=["iOS 18.0 ou posterior", "iPadOS 18.0 ou posterior", "macOS 15.0 ou posterior", "Android 8.0 ou posterior"],
    sup_h="Suporte",
    sup=f'<p>Questões ou sugestões? Escreva para <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>'
        "<p>A Alerta usa dados oficiais da proteção civil portuguesa. A sua localização nunca sai do dispositivo sem o seu consentimento.</p>",
    f_privacy="Política de Privacidade", f_terms="Termos de Utilização", f_imprint="Aviso Legal",
    f_more="Outras apps",
    rights="© 2026 Walter Tengler. Todos os direitos reservados.",
    disclaimer="Dados fornecidos pela ANEPC, pelo IPMA e pelo USGS. Esta app destina-se apenas a fins informativos e não deve ser utilizada como única fonte para decisões de emergência.",
    cl_title="Novidades da Alerta",
    cl_desc="O que mudou em cada versão da Alerta.",
    cl_h1="Novidades",
    cl_intro="O que mudou em cada versão da Alerta para iPhone, iPad e Mac. A versão Android recebe as mesmas funcionalidades, com numeração própria.",
    chip={"new": "Novo", "imp": "Melhorado", "fix": "Corrigido"},
),
"en": dict(
    title="Alerta — Real-Time Civil Protection Incidents",
    keywords="civil protection, fires, accidents, earthquakes, IPMA, Portugal, alerts, emergency, firefighters, ANEPC, citizen reports, community, iOS app, Android app",
    description="Track civil protection incidents and earthquakes in Portugal in real time. Get alerts when something new happens near you, and report incidents in your area.",
    nav_new="What's new", nav_privacy="Privacy", nav_support="Support",
    status="Official data from ANEPC and IPMA",
    h1="Civil protection alerts for your area, on your phone.",
    lede="See every ANEPC incident and IPMA earthquake on a live map. When something new happens near you, or near the places you care about, Alerta tells you right away.",
    meta="Free · iPhone, iPad, Mac and Android · 8 languages",
    play_badge="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png",
    play_alt="Get it on Google Play", apple_alt="Download on the App Store",
    hero_alt="Alerta map with active incidents across Portugal and an alert notification",
    step="Step",
    steps=[
        ("Set your area", "A radius around where you are, whole districts, or places you choose, like your parents' home."),
        ("Choose what you want to know", "Fires, accidents, floods, fallen trees, earthquakes above a magnitude. Only what matters to you."),
        ("Get the alert", "A notification with the type of incident, how far away it is and exactly where."),
    ],
    app_h="Inside the app",
    app_intro="Everything civil protection publishes, laid out to be read quickly, even under stress.",
    pairs=[
        ("06-detail", "Incident detail with resources on the ground and a timeline", None,
         "Every incident, in detail",
         "<p>Where it is, since when, what state it's in and how many resources are on the scene.</p>"
         "<ul><li>Firefighters, vehicles and aircraft</li><li>Timeline since dispatch</li><li>Severity and current status</li></ul>"),
        ("02-stats-summary", "National statistics for incidents and resources", None,
         "The country in numbers",
         "<p>Active incidents, personnel, vehicles and aircraft across Portugal, with charts for 24 hours, 30 days or a year, and by district.</p>"),
        ("04-earthquakes", "Map and list of IPMA earthquakes", None,
         "Earthquakes",
         "<p>Official IPMA data for mainland Portugal, Madeira and the Azores, and USGS data for the rest of the world. History for 24 hours, 7 or 30 days, and alerts only above the magnitude you choose.</p>"),
        ("07-new-report", "Screen for creating a report with type, location and photo", "Community",
         "Report what you see",
         "<p>A fallen tree, a blocked road, a power cut: pick the type, take a photo and send. The photo's location data is removed before it's published, and an operator reviews every report.</p>"
         "<p>Sign in with Apple or Google, or report anonymously.</p>"),
        ("08-account-reports", "Account with reputation level and list of reports", None,
         "From Civilian to Mythic",
         "<p>Ten reputation levels. Every report an operator confirms raises your trust, and invalid reports lower it. Follow your reports and your progress to the next level.</p>"
         '<div class="levels"><span>Civilian</span><span>…</span><span>Watchman</span><span>…</span><span>Mythic</span></div>'),
    ],
    more_h="More features",
    more=[
        ("Safety Circle", "Share your location with family and friends, send an SOS or tell them you're safe."),
        ("My Places", "Get alerts for places other than where you are, like your parents' home or a holiday house."),
        ("Area alerts", "Follow whole districts or ANEPC sub-regional commands."),
        ("Major incidents", "A nationwide alert when an incident draws a large response. You can turn it off."),
        ("Alerts that follow you", "Optional: the app keeps your alert area up to date in the background while you travel, even when closed."),
        ("Map legend", "Every colour and symbol explained, and an eye on incidents under observation."),
    ],
    src_h="Where the data comes from",
    src_intro="Public, official sources, checked automatically.",
    sources=[
        ("ANEPC", "Portugal's National Authority for Emergency and Civil Protection. Incidents nationwide, checked every 10 minutes."),
        ("IPMA", "Portuguese Institute for Sea and Atmosphere. Earthquakes in mainland Portugal, Madeira and the Azores."),
        ("USGS", "United States Geological Survey. Earthquakes in the rest of the world."),
        ("Community", "Reports from users, moderated by operators and always marked as such."),
    ],
    notice="Alerta is for information only and does not replace official channels. In an emergency, call <strong>112</strong>.",
    req_h="Requirements",
    req=["iOS 18.0 or later", "iPadOS 18.0 or later", "macOS 15.0 or later", "Android 8.0 or later"],
    sup_h="Support",
    sup=f'<p>Questions or feedback? Email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>'
        "<p>Alerta uses official data from Portuguese civil protection. Your location never leaves your device without your consent.</p>",
    f_privacy="Privacy Policy", f_terms="Terms of Use", f_imprint="Imprint",
    f_more="More apps",
    rights="© 2026 Walter Tengler. All rights reserved.",
    disclaimer="Data provided by ANEPC, IPMA and USGS. This app is for information only and should not be used as the only source for emergency decisions.",
    cl_title="What's New in Alerta",
    cl_desc="What changed in each version of Alerta.",
    cl_h1="What's new",
    cl_intro="What changed in each version of Alerta for iPhone, iPad and Mac. The Android version gets the same features, with its own version numbers.",
    chip={"new": "New", "imp": "Improved", "fix": "Fixed"},
),
"de": dict(
    title="Alerta — Zivilschutz-Vorfälle in Echtzeit",
    keywords="Zivilschutz, Brände, Unfälle, Erdbeben, IPMA, Portugal, Warnungen, Notfall, Feuerwehr, ANEPC, Bürgermeldungen, Community, iOS-App, Android-App",
    description="Verfolgen Sie Zivilschutz-Vorfälle und Erdbeben in Portugal in Echtzeit. Erhalten Sie Warnungen, wenn in Ihrer Nähe etwas passiert, und melden Sie Vorfälle in Ihrer Umgebung.",
    nav_new="Neuigkeiten", nav_privacy="Datenschutz", nav_support="Support",
    status="Offizielle Daten von ANEPC und IPMA",
    h1="Zivilschutz-Warnungen für Ihre Gegend, auf Ihrem Handy.",
    lede="Sehen Sie alle Einsätze der ANEPC und alle Erdbeben des IPMA auf einer Live-Karte. Wenn in Ihrer Nähe oder an Orten, die Ihnen wichtig sind, etwas passiert, warnt Alerta Sie sofort.",
    meta="Kostenlos · iPhone, iPad, Mac und Android · 8 Sprachen",
    play_badge="https://play.google.com/intl/en_us/badges/static/images/badges/de_badge_web_generic.png",
    play_alt="Jetzt bei Google Play", apple_alt="Laden im App Store",
    hero_alt="Alerta-Karte mit aktiven Einsätzen in Portugal und einer Warnmeldung",
    step="Schritt",
    steps=[
        ("Gebiet festlegen", "Ein Radius um Ihren Standort, ganze Distrikte oder Orte Ihrer Wahl, etwa das Haus Ihrer Eltern."),
        ("Auswählen, was Sie wissen wollen", "Brände, Unfälle, Überschwemmungen, umgestürzte Bäume, Erdbeben ab einer Magnitude. Nur was Sie betrifft."),
        ("Warnung erhalten", "Eine Mitteilung mit der Art des Einsatzes, der Entfernung und dem genauen Ort."),
    ],
    app_h="Was die App bietet",
    app_intro="Alles, was der Zivilschutz veröffentlicht, so aufbereitet, dass man es auch unter Stress schnell erfasst.",
    pairs=[
        ("06-detail", "Einsatzdetails mit Kräften vor Ort und Zeitverlauf", None,
         "Jeder Einsatz im Detail",
         "<p>Wo, seit wann, in welchem Stadium und wie viele Kräfte vor Ort sind.</p>"
         "<ul><li>Feuerwehrleute, Fahrzeuge und Luftfahrzeuge</li><li>Zeitverlauf seit der Alarmierung</li><li>Schweregrad und aktueller Status</li></ul>"),
        ("02-stats-summary", "Landesweite Statistik zu Einsätzen und Kräften", None,
         "Das Land in Zahlen",
         "<p>Aktive Einsätze, Einsatzkräfte, Fahrzeuge und Luftfahrzeuge in ganz Portugal, mit Diagrammen für 24 Stunden, 30 Tage oder ein Jahr, auch nach Distrikt.</p>"),
        ("04-earthquakes", "Karte und Liste der IPMA-Erdbeben", None,
         "Erdbeben",
         "<p>Offizielle IPMA-Daten für das Festland, Madeira und die Azoren, dazu USGS-Daten für den Rest der Welt. Verlauf über 24 Stunden, 7 oder 30 Tage, und Warnungen erst ab der Magnitude, die Sie wählen.</p>"),
        ("07-new-report", "Bildschirm zum Erstellen einer Meldung mit Typ, Ort und Foto", "Community",
         "Melden, was Sie sehen",
         "<p>Ein umgestürzter Baum, eine gesperrte Straße, ein Stromausfall: Typ wählen, Foto machen, absenden. Die Standortdaten des Fotos werden vor der Veröffentlichung entfernt, und jede Meldung wird von einem Moderator geprüft.</p>"
         "<p>Melden Sie sich mit Apple oder Google an, oder melden Sie anonym.</p>"),
        ("08-account-reports", "Konto mit Reputationsstufe und Liste der Meldungen", None,
         "Von Zivilist bis Mythisch",
         "<p>Zehn Reputationsstufen. Jede von einem Moderator bestätigte Meldung erhöht Ihr Vertrauen, ungültige Meldungen senken es. Verfolgen Sie Ihre Meldungen und Ihren Fortschritt zur nächsten Stufe.</p>"
         '<div class="levels"><span>Zivilist</span><span>…</span><span>Wächter</span><span>…</span><span>Mythisch</span></div>'),
    ],
    more_h="Weitere Funktionen",
    more=[
        ("Sicherheitskreis", "Teilen Sie Ihren Standort mit Familie und Freunden, senden Sie ein SOS oder melden Sie, dass Sie in Sicherheit sind."),
        ("Meine Orte", "Warnungen für andere Orte als Ihren Standort, etwa das Haus der Eltern oder die Ferienwohnung."),
        ("Gebietsalarme", "Folgen Sie ganzen Distrikten oder den Unterregionalkommandos der ANEPC."),
        ("Großeinsätze", "Eine landesweite Warnung, wenn ein Einsatz sehr viele Kräfte bindet. Lässt sich abschalten."),
        ("Warnungen, die Ihnen folgen", "Optional: Die App hält Ihr Warngebiet auf Reisen im Hintergrund aktuell, auch wenn sie geschlossen ist."),
        ("Kartenlegende", "Alle Farben und Symbole erklärt, dazu ein Auge bei Einsätzen unter Beobachtung."),
    ],
    src_h="Woher die Daten kommen",
    src_intro="Öffentliche, offizielle Quellen, automatisch abgefragt.",
    sources=[
        ("ANEPC", "Portugals nationale Behörde für Notfälle und Zivilschutz. Einsätze im ganzen Land, alle 10 Minuten abgefragt."),
        ("IPMA", "Portugiesisches Institut für Meer und Atmosphäre. Erdbeben auf dem Festland, auf Madeira und den Azoren."),
        ("USGS", "Geologischer Dienst der USA. Erdbeben im Rest der Welt."),
        ("Community", "Meldungen von Nutzern, von Moderatoren geprüft und immer als solche gekennzeichnet."),
    ],
    notice="Alerta dient nur zur Information und ersetzt keine offiziellen Kanäle. Im Notfall wählen Sie die <strong>112</strong>.",
    req_h="Voraussetzungen",
    req=["iOS 18.0 oder neuer", "iPadOS 18.0 oder neuer", "macOS 15.0 oder neuer", "Android 8.0 oder neuer"],
    sup_h="Support",
    sup=f'<p>Fragen oder Feedback? Schreiben Sie an <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>'
        "<p>Alerta nutzt offizielle Daten des portugiesischen Zivilschutzes. Ihr Standort verlässt das Gerät nie ohne Ihre Zustimmung.</p>",
    f_privacy="Datenschutzerklärung", f_terms="Nutzungsbedingungen", f_imprint="Impressum",
    f_more="Weitere Apps",
    rights="© 2026 Walter Tengler. Alle Rechte vorbehalten.",
    disclaimer="Daten von ANEPC, IPMA und USGS. Diese App dient nur zur Information und sollte nicht die einzige Grundlage für Entscheidungen im Notfall sein.",
    cl_title="Neuigkeiten in Alerta",
    cl_desc="Was sich in jeder Version von Alerta geändert hat.",
    cl_h1="Neuigkeiten",
    cl_intro="Was sich in jeder Version von Alerta für iPhone, iPad und Mac geändert hat. Die Android-Version erhält dieselben Funktionen, mit eigener Versionsnummer.",
    chip={"new": "Neu", "imp": "Verbessert", "fix": "Behoben"},
),
}

# ---------------------------------------------------------------------------
# Changelog, newest first. Each item: (kind, {lang: text}); kind is new/imp/fix.
# Version labels that are words (Summer, Spring, Launch) group older releases.
# ---------------------------------------------------------------------------
LOG = [
    dict(v={"pt": "4.3", "en": "4.3", "de": "4.3"},
         d={"pt": "novembro 2026", "en": "November 2026", "de": "November 2026"},
         t={"pt": "Alertas que o acompanham", "en": "Alerts that follow you", "de": "Warnungen, die Ihnen folgen"},
         items=[
            ("new", {"pt": "Opcional: a Alerta mantém a sua zona de alertas atualizada em segundo plano, mesmo com a app fechada, para quando viaja.",
                     "en": "Optional: Alerta keeps your alert area up to date in the background, even with the app closed, for when you travel.",
                     "de": "Optional: Alerta hält Ihr Warngebiet im Hintergrund aktuell, auch bei geschlossener App, damit es Sie auf Reisen begleitet."}),
            ("new", {"pt": "Aviso no mapa quando os dados da ANEPC têm mais de uma hora.",
                     "en": "A notice on the map when ANEPC data is more than an hour old.",
                     "de": "Ein Hinweis auf der Karte, wenn die ANEPC-Daten älter als eine Stunde sind."}),
            ("new", {"pt": "Pergunta de confirmação antes de fechar um reporte.",
                     "en": "A confirmation before you close a report.",
                     "de": "Eine Rückfrage, bevor Sie eine Meldung schließen."}),
            ("new", {"pt": "Escolhas de privacidade para anúncios, nos países onde a lei as exige.",
                     "en": "Privacy choices for ads, in the countries where the law requires them.",
                     "de": "Datenschutz-Einstellungen für Werbung in den Ländern, in denen das Gesetz sie verlangt."}),
         ]),
    dict(v={"pt": "4.2", "en": "4.2", "de": "4.2"},
         d={"pt": "16 de outubro de 2026", "en": "16 October 2026", "de": "16. Oktober 2026"},
         t={"pt": "Legenda do mapa", "en": "Map legend", "de": "Kartenlegende"},
         items=[
            ("new", {"pt": "Uma legenda explica todas as cores e símbolos do mapa.",
                     "en": "A legend explains every colour and symbol on the map.",
                     "de": "Eine Legende erklärt alle Farben und Symbole der Karte."}),
            ("imp", {"pt": "O mapa de sismos abre centrado na sua posição.",
                     "en": "The earthquake map opens centred on your location.",
                     "de": "Die Erdbebenkarte öffnet sich zentriert auf Ihren Standort."}),
         ]),
    dict(v={"pt": "4.1", "en": "4.1", "de": "4.1"},
         d={"pt": "14 de outubro de 2026", "en": "14 October 2026", "de": "14. Oktober 2026"},
         t={"pt": "Queimas controladas", "en": "Controlled burns", "de": "Kontrollierte Abbrennungen"},
         items=[
            ("new", {"pt": "Queimas e queimadas aparecem como tipo próprio, separadas dos incêndios.",
                     "en": "Controlled and agricultural burns are their own type, separate from fires.",
                     "de": "Kontrollierte und landwirtschaftliche Abbrennungen sind ein eigener Typ, getrennt von Bränden."}),
            ("imp", {"pt": "Os botões do mapa abrem as opções para o lado, sem tapar o mapa.",
                     "en": "Map buttons open their options to the side, so they don't cover the map.",
                     "de": "Die Kartenknöpfe öffnen ihre Optionen seitlich und verdecken die Karte nicht mehr."}),
         ]),
    dict(v={"pt": "4.0.2", "en": "4.0.2", "de": "4.0.2"},
         d={"pt": "6 de outubro de 2026", "en": "6 October 2026", "de": "6. Oktober 2026"},
         t={"pt": "Ajuda nos controlos do mapa", "en": "Help for map controls", "de": "Hilfe zu den Kartenknöpfen"},
         items=[
            ("imp", {"pt": "Ao primeiro toque, ou com um toque longo, cada botão do mapa explica o que faz.",
                     "en": "On first tap, or with a long press, each map button explains what it does.",
                     "de": "Beim ersten Tippen oder bei langem Drücken erklärt jeder Kartenknopf, was er tut."}),
         ]),
    dict(v={"pt": "4.0.1", "en": "4.0.1", "de": "4.0.1"},
         d={"pt": "22 de setembro de 2026", "en": "22 September 2026", "de": "22. September 2026"},
         t={"pt": "Menos ruído", "en": "Less noise", "de": "Weniger Rauschen"},
         items=[
            ("imp", {"pt": "Rescaldos passam a tipo próprio, desligado por defeito.",
                     "en": "Fire mop-up is now its own type, off by default.",
                     "de": "Nachlöscharbeiten sind ein eigener Typ, standardmäßig ausgeblendet."}),
            ("imp", {"pt": "O tipo “Outro” fica escondido por defeito.",
                     "en": "The “Other” type is hidden by default.",
                     "de": "Der Typ „Sonstiges“ ist standardmäßig ausgeblendet."}),
            ("imp", {"pt": "Alertas de polícia e radar ligados por defeito.",
                     "en": "Police and speed camera alerts are on by default.",
                     "de": "Warnungen zu Polizei und Radarkontrollen sind standardmäßig an."}),
         ]),
    dict(v={"pt": "4.0", "en": "4.0", "de": "4.0"},
         d={"pt": "16 de setembro de 2026", "en": "16 September 2026", "de": "16. September 2026"},
         t={"pt": "Alertas por zona e grandes ocorrências", "en": "Area alerts and major incidents", "de": "Gebietsalarme und Großeinsätze"},
         items=[
            ("new", {"pt": "Siga distritos inteiros ou comandos sub-regionais da ANEPC, além do seu raio.",
                     "en": "Follow whole districts or ANEPC sub-regional commands, as well as your radius.",
                     "de": "Folgen Sie ganzen Distrikten oder Unterregionalkommandos der ANEPC, zusätzlich zu Ihrem Radius."}),
            ("new", {"pt": "Alerta nacional para grandes ocorrências, que pode desativar nas Definições.",
                     "en": "A nationwide alert for major incidents, which you can turn off in Settings.",
                     "de": "Eine landesweite Warnung bei Großeinsätzen, abschaltbar in den Einstellungen."}),
            ("new", {"pt": "Um olho assinala ocorrências em vigilância.",
                     "en": "An eye marks incidents under observation.",
                     "de": "Ein Auge kennzeichnet Einsätze unter Beobachtung."}),
            ("imp", {"pt": "Nível de gravidade em vez do código de estado da ANEPC, e incêndios com as cores de estado habituais.",
                     "en": "A severity level instead of ANEPC's status code, and fires in the familiar status colours.",
                     "de": "Ein Schweregrad statt des ANEPC-Statuscodes, und Brände in den gewohnten Statusfarben."}),
            ("fix", {"pt": "Estados de ocorrência que às vezes apareciam com o nome errado.",
                     "en": "Incident statuses that sometimes showed the wrong name.",
                     "de": "Einsatzstatus, die manchmal falsch benannt waren."}),
         ]),
    dict(v={"pt": "3.5.2", "en": "3.5.2", "de": "3.5.2"},
         d={"pt": "12 de agosto de 2026", "en": "12 August 2026", "de": "12. August 2026"},
         t={"pt": "Escolha o que vê", "en": "Choose what you see", "de": "Wählen Sie, was Sie sehen"},
         items=[
            ("new", {"pt": "Escolha que tipos de ocorrência vê no mapa e de quais recebe alertas.",
                     "en": "Choose which incident types you see on the map and which ones alert you.",
                     "de": "Wählen Sie, welche Einsatztypen Sie auf der Karte sehen und bei welchen Sie gewarnt werden."}),
            ("fix", {"pt": "Alertas antigos já não se repetem ao abrir a app.",
                     "en": "Old alerts no longer repeat when you open the app.",
                     "de": "Alte Warnungen wiederholen sich beim Öffnen der App nicht mehr."}),
         ]),
    dict(v={"pt": "Verão", "en": "Summer", "de": "Sommer"},
         d={"pt": "julho de 2026", "en": "July 2026", "de": "Juli 2026"},
         t={"pt": "Mais idiomas e Meus Locais", "en": "More languages and My Places", "de": "Mehr Sprachen und Meine Orte"},
         items=[
            ("new", {"pt": "Espanhol, francês, italiano, polaco e neerlandês, além de português, inglês e alemão.",
                     "en": "Spanish, French, Italian, Polish and Dutch, alongside Portuguese, English and German.",
                     "de": "Spanisch, Französisch, Italienisch, Polnisch und Niederländisch, zusätzlich zu Portugiesisch, Englisch und Deutsch."}),
            ("new", {"pt": "Meus Locais: receba alertas para a casa dos seus pais ou a sua aldeia.",
                     "en": "My Places: get alerts for your parents' home or your village.",
                     "de": "Meine Orte: Warnungen für das Haus Ihrer Eltern oder Ihr Dorf."}),
            ("imp", {"pt": "O tamanho dos ícones reflete os meios no terreno.",
                     "en": "Icon size reflects the resources on the ground.",
                     "de": "Die Symbolgröße zeigt, wie viele Kräfte vor Ort sind."}),
            ("fix", {"pt": "Reportes de outros utilizadores que não apareciam no mapa.",
                     "en": "Reports from other users that didn't appear on the map.",
                     "de": "Meldungen anderer Nutzer, die nicht auf der Karte erschienen."}),
         ]),
    dict(v={"pt": "Primavera", "en": "Spring", "de": "Frühling"},
         d={"pt": "abril e maio de 2026", "en": "April and May 2026", "de": "April und Mai 2026"},
         t={"pt": "Reportes da comunidade", "en": "Community reports", "de": "Bürgermeldungen"},
         items=[
            ("new", {"pt": "Reporte incidentes com foto, com 10 níveis de reputação, de Civil a Mítico.",
                     "en": "Report incidents with a photo, with 10 reputation levels from Civilian to Mythic.",
                     "de": "Melden Sie Vorfälle mit Foto, mit 10 Reputationsstufen von Zivilist bis Mythisch."}),
            ("new", {"pt": "Círculo de Segurança: partilhe a sua posição com família e amigos.",
                     "en": "Safety Circle: share your location with family and friends.",
                     "de": "Sicherheitskreis: Teilen Sie Ihren Standort mit Familie und Freunden."}),
            ("new", {"pt": "Histórico de sismos de 7 e 30 dias, mais estatísticas e estatísticas por distrito.",
                     "en": "7- and 30-day earthquake history, more statistics and statistics by district.",
                     "de": "Erdbebenverlauf über 7 und 30 Tage, mehr Statistiken und Statistiken nach Distrikt."}),
            ("imp", {"pt": "Dados lidos diretamente da ANEPC.",
                     "en": "Data read directly from ANEPC.",
                     "de": "Daten direkt von der ANEPC."}),
         ]),
    dict(v={"pt": "Lançamento", "en": "Launch", "de": "Start"},
         d={"pt": "fevereiro de 2026", "en": "February 2026", "de": "Februar 2026"},
         t={"pt": "A primeira versão", "en": "The first version", "de": "Die erste Version"},
         items=[
            ("new", {"pt": "Mapa de ocorrências em tempo real, estatísticas com histórico e avisos meteorológicos.",
                     "en": "A live incident map, statistics with history, and weather warnings.",
                     "de": "Eine Live-Karte der Einsätze, Statistiken mit Verlauf und Wetterwarnungen."}),
         ]),
]

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
SHIELD = ('<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 2 4 6.5v9C4 23 9.3 28.4 16 30c6.7-1.6 12-7 12-14.5v-9L16 2z" fill="#e8552b"/>'
          '<path d="M16 9c2.6 3 4 5 4 7.5a4 4 0 0 1-8 0c0-1.4.6-2.4 1.5-3.4.2 1.3.9 2 1.7 2.2-.3-2.2.1-4.3.8-6.3z" fill="#fff"/></svg>')
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Public+Sans:wght@600;700;800&display=swap">')
HTML_LANG = {"pt": "pt", "en": "en", "de": "de"}
# Absolute base for share previews (Facebook, WhatsApp, X...): og:image must be absolute.
SITE = "https://portwally.com/Alerta/"
OG_LOCALE = {"pt": "pt_PT", "en": "en_GB", "de": "de_DE"}


def head(lang, title, description, pages, keywords=None):
    alt = "\n".join(f'    <link rel="alternate" hreflang="{l}" href="{pages[l]}">' for l in LANGS)
    kw = f'\n    <meta name="keywords" content="{escape(keywords)}">' if keywords else ""
    return f"""<!DOCTYPE html>
<html lang="{HTML_LANG[lang]}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{escape(title)}</title>{kw}
    <meta name="description" content="{escape(description)}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Alerta">
    <meta property="og:title" content="{escape(title)}">
    <meta property="og:description" content="{escape(description)}">
    <meta property="og:url" content="{SITE}{pages[lang]}">
    <meta property="og:locale" content="{OG_LOCALE[lang]}">
    <meta property="og:image" content="{SITE}share-{lang}.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="Alerta">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{SITE}share-{lang}.jpg">
    <meta name="theme-color" content="#14213d">
    {FONTS}
    <link rel="stylesheet" href="site.css">
    <link rel="icon" type="image/png" href="Alerta Banner Hero.png">
{alt}
    <script data-goatcounter="https://portwally.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head>
<body>"""


def header(lang, pages, current):
    t = T[lang]
    langs = " · ".join(f"<strong>{l.upper()}</strong>" if l == lang else f'<a href="{pages[l]}" hreflang="{l}">{l.upper()}</a>'
                       for l in LANGS)
    cur = ' aria-current="page"'
    return f"""
    <div class="tape" role="presentation"></div>
    <header class="wrap top">
        <a class="brand" href="{HOME[lang]}">{SHIELD}Alerta</a>
        <nav>
            <a href="{CHANGELOG[lang]}"{cur if current == 'changelog' else ''}>{t['nav_new']}</a>
            <a href="privacy.html">{t['nav_privacy']}</a>
            <a href="{HOME[lang]}#support">{t['nav_support']}</a>
            <span class="lang">{langs}</span>
        </nav>
    </header>"""


def footer(lang):
    t = T[lang]
    apps = "\n".join(f'            <a href="{h}">{escape(n)}</a>' for h, n in OTHER_APPS)
    return f"""
    <footer>
        <div class="wrap">
            <div class="links">
                <a href="{CHANGELOG[lang]}">{t['nav_new']}</a>
                <a href="{HOME[lang]}#support">{t['nav_support']}</a>
                <a href="privacy.html">{t['f_privacy']}</a>
                <a href="terms.html">{t['f_terms']}</a>
                <a href="imprint.html">{t['f_imprint']}</a>
            </div>
            <nav class="apps" aria-label="{t['f_more']}">
{apps}
            </nav>
            <p>{t['rights']}</p>
            <p>{t['disclaimer']}</p>
        </div>
    </footer>
</body>
</html>
"""


def badges(lang):
    t = T[lang]
    return f"""<div class="badges">
                <a href="{APP_STORE}" ping="/ping"><img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg" alt="{t['apple_alt']}" width="144" height="48"></a>
                <a href="{PLAY}" class="play" ping="/ping"><img src="{t['play_badge']}" alt="{t['play_alt']}" width="181" height="70"></a>
            </div>"""


def phone(name, alt, lazy=True):
    loading = ' loading="lazy"' if lazy else ""
    return f'<div class="phone"><img src="screenshots/web/{name}.jpg" alt="{escape(alt)}" width="1100" height="2390"{loading}></div>'


def home(lang):
    t = T[lang]
    steps = "\n".join(
        f'                <li><div class="n">{t["step"]} {i}</div><h3>{h}</h3><p>{p}</p></li>'
        for i, (h, p) in enumerate(t["steps"], 1))
    pairs = []
    for i, (img, alt, tag, h, body) in enumerate(t["pairs"]):
        flip = " flip" if i % 2 else ""
        label = f'<span class="new">{tag}</span>' if tag else ""
        pairs.append(f"""            <div class="pair{flip}">
                {phone(img, alt)}
                <div>{label}<h3>{h}</h3>{body}</div>
            </div>""")
    more = "\n".join(f"                <div><h3>{h}</h3><p>{p}</p></div>" for h, p in t["more"])
    sources = "\n".join(f"                <div><b>{h}</b><p>{p}</p></div>" for h, p in t["sources"])
    req = "".join(f"<li>{r}</li>" for r in t["req"])
    return (head(lang, t["title"], t["description"], HOME, t["keywords"]) + header(lang, HOME, "home") + f"""

    <main>
        <section class="wrap hero">
            <div>
                <span class="status"><i></i>{t['status']}</span>
                <h1>{t['h1']}</h1>
                <p class="lede">{t['lede']}</p>
                {badges(lang)}
                <p class="meta">{t['meta']}</p>
            </div>
            {phone("01-map", t["hero_alt"], lazy=False)}
        </section>

        <section class="steps">
            <ol class="wrap">
{steps}
            </ol>
        </section>

        <section class="sec">
            <div class="wrap">
            <h2>{t['app_h']}</h2>
            <p class="intro">{t['app_intro']}</p>
{chr(10).join(pairs)}
            </div>
        </section>

        <section class="sec" style="padding-top:0">
            <div class="wrap">
            <h2>{t['more_h']}</h2>
            <div class="more" style="margin-top:28px">
{more}
            </div>
            </div>
        </section>

        <section class="sec band">
            <div class="wrap">
            <h2>{t['src_h']}</h2>
            <p class="intro">{t['src_intro']}</p>
            <div class="grid">
{sources}
            </div>
            <p class="notice">{t['notice']}</p>
            </div>
        </section>

        <section class="sec" id="support">
            <div class="wrap two">
                <div><h2>{t['req_h']}</h2><ul>{req}</ul></div>
                <div><h2>{t['sup_h']}</h2>{t['sup']}</div>
            </div>
        </section>
    </main>
""" + footer(lang))


def changelog(lang):
    t = T[lang]
    entries = []
    for e in LOG:
        items = "".join(f'<li><span class="chip {k}">{t["chip"][k]}</span>{escape(txt[lang])}</li>' for k, txt in e["items"])
        entries.append(f"""            <li>
                <div class="v"><b>{escape(e['v'][lang])}</b>{escape(e['d'][lang])}</div>
                <h2>{escape(e['t'][lang])}</h2>
                <ul>{items}</ul>
            </li>""")
    return (head(lang, t["cl_title"], t["cl_desc"], CHANGELOG) + header(lang, CHANGELOG, "changelog") + f"""

    <main>
        <section class="wrap cl-head">
            <h1>{t['cl_h1']}</h1>
            <p>{t['cl_intro']}</p>
        </section>
        <section class="wrap sec" style="padding-top:40px">
            <ol class="timeline">
{chr(10).join(entries)}
            </ol>
            {badges(lang)}
        </section>
    </main>
""" + footer(lang))


if __name__ == "__main__":
    for lang in LANGS:
        (OUT / HOME[lang]).write_text(home(lang), encoding="utf-8")
        (OUT / CHANGELOG[lang]).write_text(changelog(lang), encoding="utf-8")
        print("wrote", HOME[lang], CHANGELOG[lang])
