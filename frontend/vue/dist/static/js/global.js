$(function() {
  pages = {
    'main': '<div class="row welcome"> <div class="col-md-12"> <h1>BAHNPREISE</h1> <h2>aktuelle und vergangene Ticketpreise anschauen</h2> </div> </div> <div class="btns"> <a class="btn btn-primary btn-space" href="#" onclick="switchContent(\'single_connection\');" role="button">Einzelverbindung suchen <i class="fas fa-chevron-circle-right"></i></a> <!--<a class="btn btn-primary btn-space" href="#" role="button">Streckenpreise suchen <i class="fas fa-chevron-circle-right"></i></a>--> </div> <div class="row"> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-primary shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Alle Verbindungen</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="totalConnections"></div> </div> <div class="col-auto"> <i class="fas fa-arrows-alt-h fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-primary shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Aktiv beobachtete Verbindungen</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="activeConnections"></div> </div> <div class="col-auto"> <i class="fas fa-eye fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-primary shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Verfügbare Bahnhöfe</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="stations"></div> </div> <div class="col-auto"> <i class="fas fa-city fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-primary shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Abfragen / Letzte Stunde</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="hourlyRequests"></div> </div> <div class="col-auto"> <i class="fas fa-retweet fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-primary shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Abfragen / Letzte 24 Stunden</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="dailyRequests"></div> </div> <div class="col-auto"> <i class="fas fa-arrows-alt-h fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-primary shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Durchschnittlicher Ticketpreis</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="averageCosts"></div> </div> <div class="col-auto"> <i class="fas fa-coins fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> </div> <div class="col-md-12"> <div class="card"> <div class="card-header">Wie funktioniert das alles?</div> <div class="card-body"> Die Daten die hier einsehbar sind werden von einem System permanent direkt von der Website der Bahn abgerufen. Das System gliedert sich in mehrere Teile die im nachfolgenden aufgeschlüsselt sind. <br><small>Zum besseren Verständnis einige Begriffe:<br> Verbindung (Connection): <i>Eine Reiseverbindung von Bahnhof A zu Bahnhof B zu einerm bestimmten Datum und einer bestimmten Uhrzeit. Es können mehrere Züge beinhaltet sein.</i><br> Strecke: <i>Alle Verbindungen auf einer Strecke von Bahnhof A zu Bahnhof B zu beliebiger Uhrzeit und beliebigem Datum.</i><br> Preis/Ticketpreis: <i>Preis einer Verbindung zu einem bestimmten Zeitpunkt. </i> </small> <br> <a class="btn btn-primary btn-space" href="https://github.com/bahnpreise-info/mono" role="button">Code auf GitHub <i class="fas fa-chevron-circle-right"></i></a> <br> <div class="row"> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Datenbank</div> <div class="mb-0">Die Datenbank ist das Herzstück des Systems, hier werden Bahnhöfe, Verbindungen und Preise gespeichert. Es kommt eine MySQL-Datenbank zum Einsatz.</div> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Connectionmanager</div> <div class="mb-0">Der Connectionmanager behält den Überblick über die aktiv überwachten Verbindungen. Fällt die Zahl an aktiv überwachten Verbindungen unter eine bestimmte Grenze sucht der Connectionmanager nach neuen Verbindungen. Die Wahl der Bahnhöfe und der Abfahrtszeit geschieht weitgehend zufällig.<br><small><a href="https://cubicroot.xyz">entwickelt von cubicrootxyz</a></small></div> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Scheduler </div> <div class="mb-0">Der Scheduler holt sich immer wieder neue Preise zu den aktiv überwachten Verbindungen. Sind Verbindungen ausgelaufen, also der Zug abgefahren, setzt er die Verbindungen auf inaktiv. Preise werden alle 10-26 Stunden zu zufälligen Zeitpunkten abgefragt, je näher wir dem Abfahrtszeitpunkt kommen umso öfter wird der Preis abgefragt. Die Preise erhält der Scheduler direkt von der Seite der Bahn, dank der <a href="https://github.com/kennell/schiene">Schiene Library</a>.<br><small><a href="https://cubicroot.xyz">entwickelt von cubicrootxyz</a></small></div> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">API</div> <div class="mb-0">Die Inhalte der Datenbank sind über eine JSON-API abrufbar. Die Endpunkte der API bereiten die Daten passend auf.<br><small><a href="https://stored.cc">entwickelt von storedcc</a></small></div> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Website</div> <div class="mb-0">Auf der Website bahnpreise.info sind die Daten graphisch aufbereitet und Nutzer können mit der API interagieren.<br><small>Funktionalität entwickelt von <a href="https://storedcc">storedcc</a>, Design entwickelt von <a href="https://cubicroot.xyz">cubicrootxyz</a></small></div> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">CSV-Download</div> <div class="mb-0" >Noch in Arbeit...</div> </div> </div> </div> </div> </div> </div> </div> </div> </div>',
    'single_connection': '<div class="alert alert-danger col" role="alert"> Diese Seite ist keine Seite der Deutschen Bahn oder eines anderen Bahn-Betreibers. Die aufgeführten Informationen sind unverbindlich und werden zu wissenschaftlichen Zwecken genutzt. </div> <div class="row"> <div class="col-xl-9"> <!-- Chart --> <div class="card shadow mb-4"> <div class="card-header py-3"> <h6 class="m-0 font-weight-bold text-primary" id="chart_name">Bahnpreise</h6> </div> <div class="card-body card-nopadding"> <div class="chart-area" id="bahnPriceAreachart1Top"> <canvas id="bahnPriceAreachart1"></canvas> </div> </div> </div> </div> <!-- Search beside chart --> <div class="col-xl-3"> <div class="active-pink-3 active-pink-4 mb-4"> <input class="form-control" type="text" placeholder="Suche" aria-label="Suche" id="connectionSearchBar"> <ul class="list-group" id="connectionSearchResults" style="overflow-y:scroll; max-height: 45vh"> </ul> </div> </div> </div> <!-- CARDS --> <div class="row" style="display: none;"> <div class="col row"> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-success shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Geringster Preis</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="conMinPrice">20,90€</div> </div> <div class="col-auto"> <i class="fas fa-coins fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-warning shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Durchschnittlicher Preis</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="conAvrgPrice">25,90€</div> </div> <div class="col-auto"> <i class="fas fa-coins fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-primary shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Maximaler Preis</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="conMaxPrice">45,90€</div> </div> <div class="col-auto"> <i class="fas fa-coins fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-dark shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-dark text-uppercase mb-1">Tage bis zur Abfahrt</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="conDaysLeft">0</div> </div> <div class="col-auto"> <i class="fas fa-calendar-alt fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-dark shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-dark text-uppercase mb-1">Gesammelte Datenpunkte</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="conSumPrices">10</div> </div> <div class="col-auto"> <i class="fas fa-chart-bar fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> <!-- Card --> <div class="col-xl-4 col-md-4 mb-3"> <div class="card border-left-dark shadow h-100 py-2"> <div class="card-body"> <div class="row no-gutters align-items-center"> <div class="col mr-2"> <div class="text-xs font-weight-bold text-dark text-uppercase mb-1">Größter Preissprung</div> <div class="h5 mb-0 font-weight-bold text-gray-800" id="conPriceJump">43,10€</div> </div> <div class="col-auto"> <i class="fas fa-arrows-alt-v fa-2x text-gray-300"></i> </div> </div> </div> </div> </div> </div> </div>',
    'imprint': '<div class="row"> <div class="col-md-6"> <div class="card shadow mb-4"> <div class="card-header py-3"> <h6 class="m-0 font-weight-bold text-primary">Imprint</h6> </div> <div class="card-body"> <b>Verantwortliche nach §5 TMG</b><br> Alexander Ebhart<br> Darmstädter Straße 97<br> 70376 Stuttgart<br> Mail: kontakt [at] alexander [minus] ebhart [punkt] de <br> Tel.: Null Eins Sieben Sechs Vier Sieben Eins Zwei Sieben Sechs Zwei Acht <br><br> Diese Seite wurde mit großer Sorgfalt erstellt und stellt öffentlich verfügbare Daten in aufbereiteter Form zur Verfügung. Hinter dieser Dienstleistung stehen keinerlei kommerzielle Absichten. Sollten sich dennoch Fehler oder Rechtsverstöße eingeschlichen haben bitten wir um Kontaktaufnahme und bemühen uns um eine schnellstmögliche Behebung. </div> </div> </div> <div class="col-md-6"> <!-- Area Chart --> <div class="card shadow mb-4"> <div class="card-header py-3"> <h6 class="m-0 font-weight-bold text-primary">Privacy Policy</h6> </div> <div class="card-body"> <b>Kurz und knackig ohne Schwurbelei</b><br> Wir sammeln deine Daten (IP-Adresse, Browser, etc.) nur um Missbrauch vorzubeugen und zu erkennen. Dazu noch für einige schöne Statistiken. Nach 6 Monaten ist das aber alles gelöscht. Cookies nutzen wir nur um deine Präferenzen (Sprache, Einstellungen, Favoriten, etc.) zu speichern. <br><hr><br> Diese Datenschutzerklärung klärt über Art, Zweck und Verarbeitung von personenbezogenen Daten dieses Online-Angebots und zugehöriger Funktionen auf.<br><br> <b>Verantwortlicher </b><br> Alexander Ebhart<br> Mail: kontakt [at] alexander [minus] ebhart [punkt] de <br> Tel.: Null Eins Sieben Sechs Vier Sieben Eins Zwei Sieben Sechs Zwei Acht <br><br> <b>Verarbeitete Daten</b><br> - Nutzungs- und Metadaten (z.B. IP-Adresse, Browser-Informationen, aufgerufene Seiten)<br><br> <b>Betroffene Personen</b><br> Betroffen sind alle Besucher der Website.<br><br> <b>Zweck und Rechtsgrundlage</b><br> Die Erhebung findet zum Zweck der Sicherstellung des Betriebs des Angebots statt. Hierunter fallen besonders Sicherheitsmaßnahmen.<br> Es besteht ein berechtigtes Interesse des Betreibers diese Daten zu erheben. <br><br> <b>Sicherheitsmaßnahmen und Löschung</b><br> Es werden aktuelle und branchenübliche Maßnahmen zur Sicherung der Daten genutzt. Die Daten werden nicht an Dritte weitergegeben (siehe auch Zugriffsdaten und Logs).<br> Die erhobenen Daten werden automatisiert spätestens nach 6 Monaten gelöscht. Löschungen können über die oben genannten Wege formlos beauftragt werden.<br><br> <b>Zugriffsdaten und Logs</b><br> Wir, bzw. unser Hostinganbieter, erhebt auf Grundlage unserer berechtigten Interessen im Sinne des Art. 6 Abs. 1 lit. f. DSGVO Daten über jeden Zugriff auf den Server, auf dem sich dieser Dienst befindet (sogenannte Serverlogfiles). Zu den Zugriffsdaten gehören Name der abgerufenen Webseite, Datei, Datum und Uhrzeit des Abrufs, übertragene Datenmenge, Meldung über erfolgreichen Abruf, Browsertyp nebst Version, das Betriebssystem des Nutzers, Referrer URL (die zuvor besuchte Seite), IP-Adresse und der anfragende Provider. Logfile-Informationen werden aus Sicherheitsgründen (z.B. zur Aufklärung von Missbrauchs- oder Betrugshandlungen) für die Dauer von maximal 12 Monaten gespeichert und danach gelöscht. Daten, deren weitere Aufbewahrung zu Beweiszwecken erforderlich ist, sind bis zur endgültigen Klärung des jeweiligen Vorfalls von der Löschung ausgenommen. Vom Websitebetreiber angepasst. Erstellt mit Datenschutz-Generator.de von RA Dr. Thomas Schwenke Beachten Sie bitte, dass wir Google Fonts nutzen, so wird Ihre IP-Adresse ggf. zu Google übertragen, informieren Sie sich auch über deren Datenschutz. Zudem werden anonymisierte Daten, hierzu gehören Referrer-URL, Browser, Betriebssystem, Anbieter, Zugriffsziel, Datum und Uhrzeit, statistisch aufbereitet.<br><br> <b>Rechte Betroffener</b><br> Betroffene haben das Recht auf Auskunft über erhobene Daten und deren Verarbeitung. Weiter besteht ein Recht auf Vervollständigung/Korrektur und Löschung der gespeicherten Daten. Beschwerden können an die entsprechende Aufsichtsbehörde gestellt werden. </div> </div> </div> </div>',
    'faq': '<!-- FAQ content --> <div class="container-fluid" id="faq""> <div class="row welcome"> <div class="col-md-12"> <h1>FAQ</h1> <h2>alles was du schon immer wissen wolltest</h2> </div> </div> <div class="row faq-body"> <div class="col-md-12"> <div class="card" id="q1"> <div class="card-header">Wer betreibt dieses Projekt und mit welchem Hintergrund?</div> <div class="card-body"><p>Bahnpreise.info ist ein gemeinsames Projekt von <a href="https://stored.cc">storedcc</a> und <a href="https://cubicroot.xyz">cubicrootxyz</a>, beide leidenschaftliche Bahnfahrer und Entwickler.</p><p>Erschreckenderweise finden sich auf Social-Media massenhaft unreflektierte Beschwerden über horrend teure Preise im deutschen Bahnverkehr. Zumeist buchen Menschen teure Tickets, da sie nicht mit dem Preissystem der Bahn vertraut sind. Mit diesem Tool soll Licht ins Dunkle gebracht werden und mittels Statistik die tatsächlichen Kosten für eine Bahnfahrt aufgezeigt werden.</p></div> </div> </div> </div> <div class="row faq-body"> <div class="col-md-12"> <div class="card" id="q2"> <div class="card-header">In welchem Verhältnis steht das Projekt zu Bahn-Betreibern?</div> <div class="card-body"><p>Dieses Tool ist komplett unabhängig von Bahn-Betreibern oder anderen Mobilitäts-Anbietern. Das Projekt wird ausschließlich von den beiden Entwicklern betrieben.</p></div> </div> </div> </div> <div class="row faq-body"> <div class="col-md-12"> <div class="card" id="q3"> <div class="card-header">Wie zuverlässig sind die angezeigten Preise?</div> <div class="card-body"><p>Die Preise werden direkt von der Seite des Betreibers ausgelesen, dieses Vorgehen kann aber durchaus mit Fehlern behaftet sein. Beim parsen (also dem auslesen der Betreiber-Seite) kann es zu Fehlern kommen, wenn Änderungen an der Seite vorgenommen wurden. Auch der Ausfall von Teilen der Infrastruktur des Betreibers kann zu Fehlern führen.</p><p>Der wesentliche Teil der dargestellten Preise sollte richtig sein, bei großen, kurzzeitigen Schwankungen ist aber gelegentlich mit fehlerbehafteten Daten zu rechnen.</p></div> </div> </div> </div> <div class="row faq-body"> <div class="col-md-12"> <div class="card" id="q4"> <div class="card-header">Wieso sind nicht alle Bahn-Betreiber aufgenommen?</div> <div class="card-body"><p>Das parsen (also auslesen) der Betreiber-Seite muss auf jeden Betreiber einzeln angepasst sein, das ist mit einem nicht zu missachtenden Aufwand verbunden. Zudem ist das Tool aktuell nicht dafür geeignet Preise von mehreren Seiten einzulesen. Wir haben uns daher dazu entschieden vorerst nur den größten Betreiber aufzunehmen. Alle Tickets die über dessen Website buchbar sind können auch von diesem Tool ausgewertet werden.</p></div> </div> </div> </div> <div class="row faq-body"> <div class="col-md-12"> <div class="card" id="q5"> <div class="card-header">Wie ist dieses Projekt finanziert?</div> <div class="card-body"><p>Dieses Projekt ist ausschließlich durch private Investitionen der Entwickler finanziert.</p></div> </div> </div> </div> <div class="row faq-body"> <div class="col-md-12"> <div class="card" id="q6"> <div class="card-header">In welchem Rahmen darf ich die gesammelten Daten nutzen?</div> <div class="card-body"><p>Wir freuen uns, wenn du unsere Daten weiterverwenden möchtest. Wir beschränken dies aber auf rein nicht-kommerzielle Anwendungen. Du darfst diese Daten also zu wissenschaftlichen oder privaten Zwecken nutzen, auch für ein eigenes Tool, solange du dafür kein Geld verlangst.</p></div> </div> </div> </div> <div class="row faq-body"> <div class="col-md-12"> <div class="card" id="q7"> <div class="card-header">Wohin mit meinem Verbesserungsvorschlag oder einem Bug?</div> <div class="card-body"><p>Wir entwickeln dieses Tool als Open-Source-Software, deine Anregungen kannst du uns gerne auf <a href="https://github.com/bahnpreise-info/mono">GitHub</a> zukommen lassen.</p></div> </div> </div> </div> <div class="row faq-body"> <div class="col-md-12"> <div class="card" id="q8"> <div class="card-header">Welche Verbindungen kann das Tool auswerten?</div> <div class="card-body"><p>Aktuell beschränkt sich das Tool auf Verbindungen die über die Deutsche Bahn angeboten werden. Es wird immer der günstigste Preis für die Verbindung gesucht, das ist in der Regel 2. Klasse mit (Super-)Sparpreis.</p></div> </div> </div> </div> </div> <!-- FAQ end -->',
  };
  bahnapi = new api();

  //Initial content switching based on URL
  variables = getQueryVariables();
  if (variables["site"] == null){
    switchContent("main");
  } else {
    switchContent(variables["site"]);
  }
});

//<< Dynamic Content switching >>
function switchContent(content_id, parameters) {
  $("#main_content").html(pages[content_id]);
  seturl(content_id);
  renderJsContentAsync(content_id);
}

async function renderJsContentAsync(content_id) {
  switch (content_id) {
    case "main":
      var data = bahnapi.get('/stats', {})["data"];
      $("#totalConnections").text(data["connections"]);
      $("#activeConnections").text(data["activeconnections"]);
      $("#stations").text(data["stationcount"]);
      $("#hourlyRequests").text(data["hourlyrequests"]);
      $("#dailyRequests").text(data["dailyrequests"]);
      $("#averageCosts").text(data["globalaverageprice"] + "€");
      break;
    case "single_connection":
      searchBoxListener();
      //Draw a Demo chart (If nothing precise was requested
      if (variables["connection_id"] === null || variables["connection_id"] === undefined){
        drawPricechartForConnection(0, 'bahnPriceAreachart1', true);
      } else {
        drawPricechartForConnection(variables["connection_id"], 'bahnPriceAreachart1', false);
      }
      break;
  }
}

function seturl(content_id, parameters = {}) {
  var params = "";
  $.each(parameters, function( index, value ) {
    params = index + "=" + value + "&";
  });
  window.history.pushState('Bahnpreise.info', 'Bahnpreise.info', '?site=' + content_id + "&" + params);
}
//<< Dynamic Content switching END >>

function getQueryVariables() {
  var variables = {};
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    variables[pair[0]] = pair[1];
  }
  return variables;
}

function getQueryVariable(variable) {
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    if (pair[0] == variable) {
      var value = pair[1].replace("#", "");
      return value;
    }
  }
  return null;
}


//<< Search Box JS >>
function searchBoxListener() {
  var input = $('input[id="connectionSearchBar"]');
  input.on('keyup change click', debounce(function () {
    var searchterm = $(this).val();
    if (searchterm.length <= 2) {
      return;
    }
    ShowConnections(searchterm)
  }, 200));
}

function debounce(func, wait, immediate) {
  var timeout;

  return function executedFunction() {
    var context = this;
    var args = arguments;

    var later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };

    var callNow = immediate && !timeout;

    clearTimeout(timeout);

    timeout = setTimeout(later, wait);

    if (callNow) func.apply(context, args);
  };
}
//<< Search Box JS END>>

function ShowConnections(searchterm) {
  if (typeof connections == 'undefined') {
    bahnapi = new api();
    connections = bahnapi.get('/connections/getallconnections', {});
  }
  $("#connectionSearchResults").html("");

  for (var i = 0; i < connections["data"].length; i++) {
    var obj = connections["data"][i];
    if (typeof obj === 'undefined'){
      continue;
    }
    var name = getConnectionName(obj.start, obj.end, obj.starttime);
    if (name.toLowerCase().includes(searchterm.toLowerCase())){
      $("#connectionSearchResults").append(`<button type="button" class="list-group-item list-group-item-action" onclick="drawPricechartForConnection(${obj.connection_id}, 'bahnPriceAreachart1', false);">${name}</button>`);
    }
  }
}

function getConnectionName(start, end, starttime) {
  return start + " -> " + end + " @ " + starttime;
}
