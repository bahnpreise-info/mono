webpackJsonp([1],{NHnr:function(e,t,s){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=s("7+uW"),i=s("mtWM"),r=s.n(i),n=(s("Rf8U"),{render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",{attrs:{id:"app"}},[t("router-view")],1)},staticRenderFns:[]});var d=s("VU/8")({name:"App"},n,!1,function(e){s("u22o")},null,null).exports;var c={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("nav",{staticClass:"navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow"},[s("button",{staticClass:"btn btn-link d-md-none rounded-circle mr-3",attrs:{id:"sidebarToggleTop"},on:{click:function(t){return e.someFunc()}}},[s("i",{staticClass:"fa fa-bars"}),e._v(" Menu\n    ")]),e._v(" "),s("div",{attrs:{id:"header"}}),e._v("\n    "+e._s(this.sitename)+"\n")])},staticRenderFns:[]},l=s("VU/8")({},c,!1,null,null,null).exports,o={render:function(){this.$createElement;this._self._c;return this._m(0)},staticRenderFns:[function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{staticStyle:{background:"#d10e0e"},attrs:{id:"sidebar"}},[s("ul",{staticClass:"navbar-nav bg-gradient-primary sidebar toggled sidebar-dark accordion ml-xl-auto",attrs:{id:"accordionSidebar"}},[s("a",{staticClass:"sidebar-brand d-flex align-items-center justify-content-center",attrs:{href:"/#/"}},[s("div",{staticClass:"sidebar-brand-icon"},[s("i",{staticClass:"fas fa-subway"})]),e._v(" "),s("div",{staticClass:"sidebar-brand-text mx-2"},[e._v("Bahnpreise.info")])]),e._v(" "),s("hr",{staticClass:"sidebar-divider my-0"}),e._v(" "),s("li",{staticClass:"nav-item"},[s("a",{staticClass:"nav-link",attrs:{href:"/#/"}},[s("i",{staticClass:"fas fa-fw fa-home"}),e._v(" "),s("span",[e._v("Home")])])]),e._v(" "),s("hr",{staticClass:"sidebar-divider"}),e._v(" "),s("div",{staticClass:"sidebar-heading"},[e._v("\n            Abfragen\n        ")]),e._v(" "),s("li",{staticClass:"nav-item"},[s("a",{staticClass:"nav-link",attrs:{href:"/#/single_connection"}},[s("i",{staticClass:"fas fa-fw fa-long-arrow-alt-right"}),e._v(" "),s("span",[e._v("Einzelverbindung")])])]),e._v(" "),s("li",{staticClass:"nav-item"},[s("a",{staticClass:"nav-link"},[s("i",{staticClass:"fas fa-fw fa-arrows-alt-h"}),e._v(" "),s("span",[e._v("Strecken (kommt bald)")])])]),e._v(" "),s("li",{staticClass:"nav-item"},[s("a",{staticClass:"nav-link"},[s("i",{staticClass:"fas fa-fw fa-arrows-alt"}),e._v(" "),s("span",[e._v("Statistik (kommt bald)")])])]),e._v(" "),s("hr",{staticClass:"sidebar-divider"}),e._v(" "),s("div",{staticClass:"sidebar-heading"},[e._v("\n            Sonstiges\n        ")]),e._v(" "),s("li",{staticClass:"nav-item"},[s("a",{staticClass:"nav-link",attrs:{href:"/#/faq"}},[s("i",{staticClass:"fas fa-fw fa-question-circle"}),e._v(" "),s("span",[e._v("FAQ")])])]),e._v(" "),s("hr",{staticClass:"sidebar-divider d-none d-md-block"}),e._v(" "),s("div",{staticClass:"text-center d-none d-md-inline"},[s("button",{staticClass:"rounded-circle border-0",attrs:{id:"sidebarToggle"}})])])])}]},v=s("VU/8")({name:"sidebar"},o,!1,null,null,null).exports,h={render:function(){this.$createElement;this._self._c;return this._m(0)},staticRenderFns:[function(){var e=this.$createElement,t=this._self._c||e;return t("footer",{staticClass:"sticky-footer bg-white"},[t("div",{staticClass:"container my-auto"},[t("div",{staticClass:"copyright text-center my-auto"},[t("a",{attrs:{href:"/#/imprint"}},[this._v("Imprint | Privacy Policy")]),t("br"),this._v(" "),t("span",[this._v("Copyright © storedcc & cubicrootxyz 2019")])])])])}]},u=s("VU/8")(null,h,!1,null,null,null).exports,b=s("/ocq"),m={name:"home",methods:{updateStats(){r.a.get(this.apiUrl+"/stats").then(e=>{console.log(e.data),this.stats=e.data})}},data:()=>({stats:{data:{activeconnections:0,stationcount:0,hourlyrequests:0,connections:0,dailyrequests:0,globalaverageprice:0}}}),mounted(){this.updateStats()}},g={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{staticClass:"home"},[e._m(0),e._v(" "),e._m(1),e._v(" "),s("div",{staticClass:"container-fluid"},[s("div",{staticClass:"row"},[s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-primary shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("Alle Verbindungen")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"totalConnections"}},[e._v(e._s(this.stats.data.connections))])]),e._v(" "),e._m(2)])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-primary shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("Aktiv beobachtete Verbindungen")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"activeConnections"}},[e._v(e._s(this.stats.data.activeconnections))])]),e._v(" "),e._m(3)])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-primary shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("Verfügbare Bahnhöfe")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"stations"}},[e._v(e._s(this.stats.data.stationcount))])]),e._v(" "),e._m(4)])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-primary shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("Abfragen / Letzte Stunde")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"hourlyRequests"}},[e._v(e._s(this.stats.data.hourlyrequests))])]),e._v(" "),e._m(5)])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-primary shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("Abfragen / Letzte 24 Stunden")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"dailyRequests"}},[e._v(e._s(this.stats.data.dailyrequests))])]),e._v(" "),e._m(6)])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-primary shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("Durchschnittlicher Ticketpreis")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"averageCosts"}},[e._v(e._s(this.stats.data.globalaverageprice))])]),e._v(" "),e._m(7)])])])])])]),e._v(" "),e._m(8)])},staticRenderFns:[function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"row welcome"},[t("div",{staticClass:"col-md-12"},[t("h1",[this._v("BAHNPREISE")]),this._v(" "),t("h2",[this._v("Aktuelle und vergangene Ticketpreise anschauen")])])])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"btns"},[t("a",{staticClass:"btn btn-primary btn-space",attrs:{href:"/#/single_connection",onclick:"",role:"button"}},[this._v("Einzelverbindung suchen\n            "),t("i",{staticClass:"fas fa-chevron-circle-right"})])])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"col-auto"},[t("i",{staticClass:"fas fa-arrows-alt-h fa-2x text-gray-300"})])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"col-auto"},[t("i",{staticClass:"fas fa-eye fa-2x text-gray-300"})])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"col-auto"},[t("i",{staticClass:"fas fa-city fa-2x text-gray-300"})])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"col-auto"},[t("i",{staticClass:"fas fa-retweet fa-2x text-gray-300"})])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"col-auto"},[t("i",{staticClass:"fas fa-arrows-alt-h fa-2x text-gray-300"})])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"col-auto"},[t("i",{staticClass:"fas fa-coins fa-2x text-gray-300"})])},function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{staticClass:"col-md-12"},[s("div",{staticClass:"card"},[s("div",{staticClass:"card-header"},[e._v("Wie funktioniert das alles?")]),e._v(" "),s("div",{staticClass:"card-body"},[e._v(" Die Daten die hier einsehbar sind werden von einem System permanent direkt von der Website der Bahn abgerufen. Das System gliedert sich in mehrere Teile die im nachfolgenden aufgeschlüsselt sind.\n                "),s("br"),s("small",[e._v("Zum besseren Verständnis einige Begriffe:"),s("br"),e._v(" Verbindung (Connection): "),s("i",[e._v("Eine Reiseverbindung von Bahnhof A zu Bahnhof B zu einerm bestimmten Datum und einer bestimmten Uhrzeit. Es können mehrere Züge beinhaltet sein.")]),s("br"),e._v(" Strecke: "),s("i",[e._v("Alle Verbindungen auf einer Strecke von Bahnhof A zu Bahnhof B zu beliebiger Uhrzeit und beliebigem Datum.")]),s("br"),e._v(" Preis/Ticketpreis: "),s("i",[e._v("Preis einer Verbindung zu einem bestimmten Zeitpunkt. ")])]),e._v(" "),s("br"),e._v(" "),s("a",{staticClass:"btn btn-primary btn-space",attrs:{href:"https://github.com/bahnpreise-info/mono",role:"button"}},[e._v("Code auf GitHub "),s("i",{staticClass:"fas fa-chevron-circle-right"})]),e._v(" "),s("br"),e._v(" "),s("div",{staticClass:"row"},[s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("Datenbank")]),e._v(" "),s("div",{staticClass:"mb-0"},[e._v("Die Datenbank ist das Herzstück des Systems, hier werden Bahnhöfe, Verbindungen und Preise gespeichert. Es kommt eine MySQL-Datenbank zum Einsatz.")])])])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("Connectionmanager")]),e._v(" "),s("div",{staticClass:"mb-0"},[e._v("Der Connectionmanager behält den Überblick über die aktiv überwachten Verbindungen. Fällt die Zahl an aktiv überwachten Verbindungen unter eine bestimmte Grenze sucht der Connectionmanager nach neuen Verbindungen. Die Wahl der Bahnhöfe und der Abfahrtszeit geschieht weitgehend zufällig.\n                                            "),s("br"),s("small",[s("a",{attrs:{href:"https://cubicroot.xyz"}},[e._v("entwickelt von cubicrootxyz")])])])])])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("Scheduler ")]),e._v(" "),s("div",{staticClass:"mb-0"},[e._v("Der Scheduler holt sich immer wieder neue Preise zu den aktiv überwachten Verbindungen. Sind Verbindungen ausgelaufen, also der Zug abgefahren, setzt er die Verbindungen auf inaktiv. Preise werden alle 10-26 Stunden zu zufälligen Zeitpunkten abgefragt, je näher wir dem Abfahrtszeitpunkt kommen umso öfter wird der Preis abgefragt. Die Preise erhält der Scheduler direkt von der Seite der Bahn, dank der "),s("a",{attrs:{href:"https://github.com/kennell/schiene"}},[e._v("Schiene Library")]),e._v(".\n                                            "),s("br"),s("small",[s("a",{attrs:{href:"https://cubicroot.xyz"}},[e._v("entwickelt von cubicrootxyz")])])])])])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("API")]),e._v(" "),s("div",{staticClass:"mb-0"},[e._v("Die Inhalte der Datenbank sind über eine JSON-API abrufbar. Die Endpunkte der API bereiten die Daten passend auf.\n                                            "),s("br"),s("small",[s("a",{attrs:{href:"https://stored.cc"}},[e._v("entwickelt von storedcc")])])])])])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("Website")]),e._v(" "),s("div",{staticClass:"mb-0"},[e._v("Auf der Website bahnpreise.info sind die Daten graphisch aufbereitet und Nutzer können mit der API interagieren.\n                                            "),s("br"),s("small",[e._v("Funktionalität entwickelt von "),s("a",{attrs:{href:"https://storedcc"}},[e._v("storedcc")]),e._v(", Design entwickelt von "),s("a",{attrs:{href:"https://cubicroot.xyz"}},[e._v("cubicrootxyz")])])])])])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("CSV-Download")]),e._v(" "),s("div",{staticClass:"mb-0"},[e._v("Noch in Arbeit...")])])])])])])])])])])}]};var f=s("VU/8")(m,g,!1,function(e){s("OTz8")},"data-v-cb87c072",null).exports,_={render:function(){this.$createElement;this._self._c;return this._m(0)},staticRenderFns:[function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",[s("div",{staticClass:"container-fluid",attrs:{id:"faq"}},[s("div",{staticClass:"row welcome "},[s("div",{staticClass:"col-md-12 "},[s("h1",[e._v("FAQ")]),e._v(" "),s("h2",[e._v("alles was du schon immer wissen wolltest")])])]),e._v(" "),s("div",{staticClass:"row faq-body "},[s("div",{staticClass:"col-md-12 "},[s("div",{staticClass:"card ",attrs:{id:"q1 "}},[s("div",{staticClass:"card-header "},[e._v("Wer betreibt dieses Projekt und mit welchem Hintergrund?")]),e._v(" "),s("div",{staticClass:"card-body "},[s("p",[e._v("Bahnpreise.info ist ein gemeinsames Projekt von "),s("a",{attrs:{href:"https://stored.cc "}},[e._v("storedcc")]),e._v(" und "),s("a",{attrs:{href:"https://cubicroot.xyz "}},[e._v("cubicrootxyz")]),e._v(", beide leidenschaftliche Bahnfahrer und Entwickler.")]),e._v(" "),s("p",[e._v("Erschreckenderweise finden sich auf Social-Media massenhaft unreflektierte Beschwerden über horrend teure Preise im deutschen Bahnverkehr. Zumeist buchen Menschen teure Tickets, da sie nicht mit dem Preissystem der Bahn vertraut sind. Mit diesem Tool soll Licht ins Dunkle gebracht werden und mittels Statistik die tatsächlichen Kosten für eine Bahnfahrt aufgezeigt werden.")])])])])]),e._v(" "),s("div",{staticClass:"row faq-body "},[s("div",{staticClass:"col-md-12 "},[s("div",{staticClass:"card ",attrs:{id:"q2 "}},[s("div",{staticClass:"card-header "},[e._v("In welchem Verhältnis steht das Projekt zu Bahn-Betreibern?")]),e._v(" "),s("div",{staticClass:"card-body "},[s("p",[e._v("Dieses Tool ist komplett unabhängig von Bahn-Betreibern oder anderen Mobilitäts-Anbietern. Das Projekt wird ausschließlich von den beiden Entwicklern betrieben.")])])])])]),e._v(" "),s("div",{staticClass:"row faq-body "},[s("div",{staticClass:"col-md-12 "},[s("div",{staticClass:"card ",attrs:{id:"q3 "}},[s("div",{staticClass:"card-header "},[e._v("Wie zuverlässig sind die angezeigten Preise?")]),e._v(" "),s("div",{staticClass:"card-body "},[s("p",[e._v("Die Preise werden direkt von der Seite des Betreibers ausgelesen, dieses Vorgehen kann aber durchaus mit Fehlern behaftet sein. Beim parsen (also dem auslesen der Betreiber-Seite) kann es zu Fehlern kommen, wenn Änderungen an der Seite vorgenommen wurden. Auch der Ausfall von Teilen der Infrastruktur des Betreibers kann zu Fehlern führen.")]),e._v(" "),s("p",[e._v("Der wesentliche Teil der dargestellten Preise sollte richtig sein, bei großen, kurzzeitigen Schwankungen ist aber gelegentlich mit fehlerbehafteten Daten zu rechnen.")])])])])]),e._v(" "),s("div",{staticClass:"row faq-body "},[s("div",{staticClass:"col-md-12 "},[s("div",{staticClass:"card ",attrs:{id:"q4 "}},[s("div",{staticClass:"card-header "},[e._v("Wieso sind nicht alle Bahn-Betreiber aufgenommen?")]),e._v(" "),s("div",{staticClass:"card-body "},[s("p",[e._v("Das parsen (also auslesen) der Betreiber-Seite muss auf jeden Betreiber einzeln angepasst sein, das ist mit einem nicht zu missachtenden Aufwand verbunden. Zudem ist das Tool aktuell nicht dafür geeignet Preise von mehreren Seiten einzulesen. Wir haben uns daher dazu entschieden vorerst nur den größten Betreiber aufzunehmen. Alle Tickets die über dessen Website buchbar sind können auch von diesem Tool ausgewertet werden.")])])])])]),e._v(" "),s("div",{staticClass:"row faq-body "},[s("div",{staticClass:"col-md-12 "},[s("div",{staticClass:"card ",attrs:{id:"q5 "}},[s("div",{staticClass:"card-header "},[e._v("Wie ist dieses Projekt finanziert?")]),e._v(" "),s("div",{staticClass:"card-body "},[s("p",[e._v("Dieses Projekt ist ausschließlich durch private Investitionen der Entwickler finanziert.")])])])])]),e._v(" "),s("div",{staticClass:"row faq-body "},[s("div",{staticClass:"col-md-12 "},[s("div",{staticClass:"card ",attrs:{id:"q6 "}},[s("div",{staticClass:"card-header "},[e._v("In welchem Rahmen darf ich die gesammelten Daten nutzen?")]),e._v(" "),s("div",{staticClass:"card-body "},[s("p",[e._v("Wir freuen uns, wenn du unsere Daten weiterverwenden möchtest. Wir beschränken dies aber auf rein nicht-kommerzielle Anwendungen. Du darfst diese Daten also zu wissenschaftlichen oder privaten Zwecken nutzen, auch für ein eigenes Tool, solange du dafür kein Geld verlangst.")])])])])]),e._v(" "),s("div",{staticClass:"row faq-body "},[s("div",{staticClass:"col-md-12 "},[s("div",{staticClass:"card ",attrs:{id:"q7 "}},[s("div",{staticClass:"card-header "},[e._v("Wohin mit meinem Verbesserungsvorschlag oder einem Bug?")]),e._v(" "),s("div",{staticClass:"card-body "},[s("p",[e._v("Wir entwickeln dieses Tool als Open-Source-Software, deine Anregungen kannst du uns gerne auf "),s("a",{attrs:{href:"https://github.com/bahnpreise-info/mono "}},[e._v("GitHub")]),e._v(" zukommen lassen.")])])])])]),e._v(" "),s("div",{staticClass:"row faq-body "},[s("div",{staticClass:"col-md-12 "},[s("div",{staticClass:"card ",attrs:{id:"q8 "}},[s("div",{staticClass:"card-header "},[e._v("Welche Verbindungen kann das Tool auswerten?")]),e._v(" "),s("div",{staticClass:"card-body "},[s("p",[e._v("Aktuell beschränkt sich das Tool auf Verbindungen die über die Deutsche Bahn angeboten werden. Es wird immer der günstigste Preis für die Verbindung gesucht, das ist in der Regel 2. Klasse mit (Super-)Sparpreis.")])])])])])])])}]},C=s("VU/8")(null,_,!1,null,null,null).exports,p={render:function(){this.$createElement;this._self._c;return this._m(0)},staticRenderFns:[function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",[s("div",{staticClass:"row"},[s("div",{staticClass:"col-md-6"},[s("div",{staticClass:"card shadow mb-4"},[s("div",{staticClass:"card-header py-3"},[s("h6",{staticClass:"m-0 font-weight-bold text-primary"},[e._v("Imprint")])]),e._v(" "),s("div",{staticClass:"card-body"},[s("b",[e._v("Verantwortliche nach §5 TMG")]),e._v(" "),s("br"),e._v(" Alexander Ebhart\n                    "),s("br"),e._v(" Darmstädter Straße 97\n                    "),s("br"),e._v(" 70376 Stuttgart\n                    "),s("br"),e._v(" Mail: kontakt [at] alexander [minus] ebhart [punkt] de\n                    "),s("br"),e._v(" Tel.: Null Eins Sieben Sechs Vier Sieben Eins Zwei Sieben Sechs Zwei Acht\n                    "),s("br"),e._v(" "),s("br"),e._v(" Diese Seite wurde mit großer Sorgfalt erstellt und stellt öffentlich verfügbare Daten in aufbereiteter Form zur Verfügung. Hinter dieser Dienstleistung stehen keinerlei kommerzielle Absichten. Sollten sich dennoch Fehler oder Rechtsverstöße eingeschlichen haben bitten wir um Kontaktaufnahme und bemühen uns um eine schnellstmögliche Behebung. ")])])]),e._v(" "),s("div",{staticClass:"col-md-6"},[s("div",{staticClass:"card shadow mb-4"},[s("div",{staticClass:"card-header py-3"},[s("h6",{staticClass:"m-0 font-weight-bold text-primary"},[e._v("Privacy Policy")])]),e._v(" "),s("div",{staticClass:"card-body"},[s("b",[e._v("Kurz und knackig ohne Schwurbelei")]),e._v(" "),s("br"),e._v(" Wir sammeln deine Daten (IP-Adresse, Browser, etc.) nur um Missbrauch vorzubeugen und zu erkennen. Dazu noch für einige schöne Statistiken. Nach 6 Monaten ist das aber alles gelöscht. Cookies nutzen wir nur um deine Präferenzen (Sprache, Einstellungen, Favoriten, etc.) zu speichern.\n                    "),s("br"),e._v(" "),s("hr"),e._v(" "),s("br"),e._v(" Diese Datenschutzerklärung klärt über Art, Zweck und Verarbeitung von personenbezogenen Daten dieses Online-Angebots und zugehöriger Funktionen auf.\n                    "),s("br"),e._v(" "),s("br"),e._v(" "),s("b",[e._v("Verantwortlicher ")]),e._v(" "),s("br"),e._v(" Alexander Ebhart\n                    "),s("br"),e._v(" Mail: kontakt [at] alexander [minus] ebhart [punkt] de\n                    "),s("br"),e._v(" Tel.: Null Eins Sieben Sechs Vier Sieben Eins Zwei Sieben Sechs Zwei Acht\n                    "),s("br"),e._v(" "),s("br"),e._v(" "),s("b",[e._v("Verarbeitete Daten")]),e._v(" "),s("br"),e._v(" - Nutzungs- und Metadaten (z.B. IP-Adresse, Browser-Informationen, aufgerufene Seiten)\n                    "),s("br"),e._v(" "),s("br"),e._v(" "),s("b",[e._v("Betroffene Personen")]),e._v(" "),s("br"),e._v(" Betroffen sind alle Besucher der Website.\n                    "),s("br"),e._v(" "),s("br"),e._v(" "),s("b",[e._v("Zweck und Rechtsgrundlage")]),e._v(" "),s("br"),e._v(" Die Erhebung findet zum Zweck der Sicherstellung des Betriebs des Angebots statt. Hierunter fallen besonders Sicherheitsmaßnahmen.\n                    "),s("br"),e._v(" Es besteht ein berechtigtes Interesse des Betreibers diese Daten zu erheben.\n                    "),s("br"),e._v(" "),s("br"),e._v(" "),s("b",[e._v("Sicherheitsmaßnahmen und Löschung")]),e._v(" "),s("br"),e._v(" Es werden aktuelle und branchenübliche Maßnahmen zur Sicherung der Daten genutzt. Die Daten werden nicht an Dritte weitergegeben (siehe auch Zugriffsdaten und Logs).\n                    "),s("br"),e._v(" Die erhobenen Daten werden automatisiert spätestens nach 6 Monaten gelöscht. Löschungen können über die oben genannten Wege formlos beauftragt werden.\n                    "),s("br"),e._v(" "),s("br"),e._v(" "),s("b",[e._v("Zugriffsdaten und Logs")]),e._v(" "),s("br"),e._v(" Wir, bzw. unser Hostinganbieter, erhebt auf Grundlage unserer berechtigten Interessen im Sinne des Art. 6 Abs. 1 lit. f. DSGVO Daten über jeden Zugriff auf den Server, auf dem sich dieser Dienst befindet (sogenannte Serverlogfiles). Zu den Zugriffsdaten gehören Name der abgerufenen Webseite, Datei, Datum und Uhrzeit des Abrufs, übertragene Datenmenge, Meldung über erfolgreichen Abruf, Browsertyp nebst Version, das Betriebssystem des Nutzers, Referrer URL (die zuvor besuchte Seite), IP-Adresse und der anfragende Provider. Logfile-Informationen werden aus Sicherheitsgründen (z.B. zur Aufklärung von Missbrauchs- oder Betrugshandlungen) für die Dauer von maximal 12 Monaten gespeichert und danach gelöscht. Daten, deren weitere Aufbewahrung zu Beweiszwecken erforderlich ist, sind bis zur endgültigen Klärung des jeweiligen Vorfalls von der Löschung ausgenommen. Vom Websitebetreiber angepasst. Erstellt mit Datenschutz-Generator.de von RA Dr. Thomas Schwenke Beachten Sie bitte, dass wir Google Fonts nutzen, so wird Ihre IP-Adresse ggf. zu Google übertragen, informieren Sie sich auch über deren Datenschutz. Zudem werden anonymisierte Daten, hierzu gehören Referrer-URL, Browser, Betriebssystem, Anbieter, Zugriffsziel, Datum und Uhrzeit, statistisch aufbereitet.\n                    "),s("br"),e._v(" "),s("br"),e._v(" "),s("b",[e._v("Rechte Betroffener")]),e._v(" "),s("br"),e._v(" Betroffene haben das Recht auf Auskunft über erhobene Daten und deren Verarbeitung. Weiter besteht ein Recht auf Vervollständigung/Korrektur und Löschung der gespeicherten Daten. Beschwerden können an die entsprechende Aufsichtsbehörde gestellt werden. ")])])])])])}]},w=s("VU/8")(null,p,!1,null,null,null).exports;function y(e,t,s,a){e=(e+"").replace(",","").replace(" ","");var i=isFinite(+e)?+e:0,r=isFinite(+t)?Math.abs(t):0,n=void 0===a?",":a,d=void 0===s?".":s,c="";return(c=(r?function(e,t){var s=Math.pow(10,t);return""+Math.round(e*s)/s}(i,r):""+Math.round(i)).split("."))[0].length>3&&(c[0]=c[0].replace(/\B(?=(?:\d{3})+(?!\d))/g,n)),(c[1]||"").length<r&&(c[1]=c[1]||"",c[1]+=new Array(r-c[1].length+1).join("0")),c.join(d)}var x={name:"home",computed:{},data:()=>({chart_name:"Bahnpreise",disclaimer:"Diese Seite ist keine Seite der Deutschen Bahn oder eines anderen Bahn-Betreibers. Die aufgeführten Informationen sind unverbindlich und werden zu wissenschaftlichen Zwecken genutzt.",searchQuery:"",searchresults:{}}),methods:{submitSearch(){r.a.get(this.apiUrl+"/connections/getallconnections").then(e=>{let t=e.data;this.searchresults={};for(let e=0;e<t.data.length;e++){let s=t.data[e];if(void 0===s)continue;let a=s.start+" -> "+s.end+" @ "+s.starttime;a.toLowerCase().includes(this.searchQuery.toLowerCase())&&(this.searchresults[s.connection_id]=a)}})},removeSearchQuery:function(){this.searchQuery="",this.searchresults={}},getChartData:function(e=null){if(null===e)r.a.get(this.apiUrl+"/connections/getrandomconnection").then(e=>{this.data=e,this.renderChart()});else{let t=new URLSearchParams;t.append("connection_id",e),r.a.get(this.apiUrl+"/prices",{params:t}).then(e=>{this.data=e,this.renderChart()})}},renderChart:function(){Chart.defaults.global.defaultFontFamily="Nunito",Chart.defaults.global.defaultFontColor="#858796";let e=[],t=[],s=[];$.each(this.data.data.data.prices_days_to_departure,function(t,s){e.push(t)}),e.sort(function(e,t){return t-e});for(var a=0;a<e.length;a++)t.push(e[a]+" Tage");for(a=0;a<e.length;a++)s.push(this.data.data.data.prices_days_to_departure[e[a]]);this.chart_name=this.data.data.data.start+" -> "+this.data.data.data.end+" @ "+this.data.data.data.starttime,$("#bahnPriceAreachart1").remove(),$("#bahnPriceAreachart1Top").html('<canvas id="bahnPriceAreachart1"></canvas>');let i=document.getElementById("bahnPriceAreachart1");new Chart(i,{type:"line",data:{labels:t,datasets:[{label:"Preis",lineTension:.3,backgroundColor:"rgba(209,14,14, 0.05)",borderColor:"#d10e0e",pointRadius:3,pointBackgroundColor:"#d10e0e",pointBorderColor:"#d10e0e",pointHoverRadius:3,pointHoverBackgroundColor:"rgba(78, 115, 223, 1)",pointHoverBorderColor:"rgba(78, 115, 223, 1)",pointHitRadius:10,pointBorderWidth:2,data:s}]},options:{elements:{line:{cubicInterpolationMode:"monotone"}},maintainAspectRatio:!1,layout:{padding:{left:10,right:25,top:25,bottom:0}},scales:{xAxes:[{time:{unit:"date"},gridLines:{display:!1,drawBorder:!1},ticks:{maxTicksLimit:7}}],yAxes:[{ticks:{maxTicksLimit:5,padding:10,callback:function(e,t,s){return"€"+y(e,2)}},gridLines:{color:"rgb(234, 236, 244)",zeroLineColor:"rgb(234, 236, 244)",drawBorder:!1,borderDash:[2],zeroLineBorderDash:[2]}}]},legend:{display:!1},tooltips:{backgroundColor:"rgb(255,255,255)",bodyFontColor:"#858796",titleMarginBottom:10,titleFontColor:"#6e707e",titleFontSize:14,borderColor:"#d10e0e",borderWidth:1,xPadding:15,yPadding:15,displayColors:!1,intersect:!1,mode:"index",caretPadding:10,callbacks:{label:function(e,t){return(t.datasets[e.datasetIndex].label||"")+": €"+y(e.yLabel,2)}}}}})}},mounted(){this.getChartData()}},k={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",[s("div",{staticClass:"alert alert-danger col",attrs:{role:"alert"}},[e._v(e._s(e.disclaimer))]),e._v(" "),s("div",{staticClass:"row"},[s("div",{staticClass:"col-xl-9"},[s("div",{staticClass:"card shadow mb-4"},[s("div",{staticClass:"card-header py-3"},[s("h6",{staticClass:"m-0 font-weight-bold text-primary",attrs:{id:"chart_name"}},[e._v(e._s(e.chart_name))])]),e._v(" "),e._m(0)])]),e._v(" "),s("div",{staticClass:"col-xl-3"},[s("div",{staticClass:"col-sm-auto",staticStyle:{"padding-bottom":"1em"}},[s("button",{staticClass:"btn btn-primary btn-lg btn-block",attrs:{type:"button"},on:{click:function(t){return e.getChartData()}}},[e._v("Zufällige Verbindung suchen")])]),e._v(" "),s("div",{staticClass:"col-sm-auto",staticStyle:{"padding-bottom":"1em"}},[s("form",{staticClass:"searchForm",on:{submit:function(t){return t.preventDefault(),e.submitSearch()}}},[s("input",{directives:[{name:"model",rawName:"v-model",value:e.searchQuery,expression:"searchQuery"}],staticClass:"form-control",attrs:{type:"text",placeholder:"Suche"},domProps:{value:e.searchQuery},on:{keyup:function(t){return e.submitSearch()},input:function(t){t.target.composing||(e.searchQuery=t.target.value)}}})])]),e._v(" "),s("div",{staticClass:"col-sm-auto",staticStyle:{"overflow-y":"scroll","max-height":"50vh"}},e._l(e.searchresults,function(t,a){return s("ul",{staticClass:"list-group",attrs:{id:"connectionSearchResults"}},[s("button",{staticClass:"list-group-item list-group-item-action",attrs:{type:"button"},on:{click:function(t){return e.getChartData(a)}}},[e._v(e._s(t))])])}),0)])]),e._v(" "),e._m(1),e._v("'\n")])},staticRenderFns:[function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"card-body card-nopadding"},[t("div",{staticClass:"chart-area",attrs:{id:"bahnPriceAreachart1Top"}},[t("canvas",{attrs:{id:"bahnPriceAreachart1"}})])])},function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{staticClass:"row",staticStyle:{display:"none"}},[s("div",{staticClass:"col row"},[s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-success shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-success text-uppercase mb-1"},[e._v("Geringster Preis")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"conMinPrice"}},[e._v("20,90€")])]),e._v(" "),s("div",{staticClass:"col-auto"},[s("i",{staticClass:"fas fa-coins fa-2x text-gray-300"})])])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-warning shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-warning text-uppercase mb-1"},[e._v("Durchschnittlicher Preis")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"conAvrgPrice"}},[e._v("25,90€")])]),e._v(" "),s("div",{staticClass:"col-auto"},[s("i",{staticClass:"fas fa-coins fa-2x text-gray-300"})])])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-primary shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-primary text-uppercase mb-1"},[e._v("Maximaler Preis")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"conMaxPrice"}},[e._v("45,90€")])]),e._v(" "),s("div",{staticClass:"col-auto"},[s("i",{staticClass:"fas fa-coins fa-2x text-gray-300"})])])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-dark shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-dark text-uppercase mb-1"},[e._v("Tage bis zur Abfahrt")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"conDaysLeft"}},[e._v("0")])]),e._v(" "),s("div",{staticClass:"col-auto"},[s("i",{staticClass:"fas fa-calendar-alt fa-2x text-gray-300"})])])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-dark shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-dark text-uppercase mb-1"},[e._v("Gesammelte Datenpunkte")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"conSumPrices"}},[e._v("10")])]),e._v(" "),s("div",{staticClass:"col-auto"},[s("i",{staticClass:"fas fa-chart-bar fa-2x text-gray-300"})])])])])]),e._v(" "),s("div",{staticClass:"col-xl-4 col-md-4 mb-3"},[s("div",{staticClass:"card border-left-dark shadow h-100 py-2"},[s("div",{staticClass:"card-body"},[s("div",{staticClass:"row no-gutters align-items-center"},[s("div",{staticClass:"col mr-2"},[s("div",{staticClass:"text-xs font-weight-bold text-dark text-uppercase mb-1"},[e._v("Größter Preissprung")]),e._v(" "),s("div",{staticClass:"h5 mb-0 font-weight-bold text-gray-800",attrs:{id:"conPriceJump"}},[e._v("43,10€")])]),e._v(" "),s("div",{staticClass:"col-auto"},[s("i",{staticClass:"fas fa-arrows-alt-v fa-2x text-gray-300"})])])])])])])])}]},z=s("VU/8")(x,k,!1,null,null,null).exports;a.a.use(b.a);var S=new b.a({routes:[{path:"/",name:"/home",component:f},{path:"/single_connection",name:"/single_connection",component:z},{path:"/faq",name:"/faq",component:C},{path:"/imprint",name:"/imprint",component:w}]});a.a.config.productionTip=!1,a.a.mixin({computed:{},data:function(){return{sitename:"Bahnpreise.info",get apiUrl(){return"https://api.bahnpreise.info"}}}}),new a.a({el:"#header",components:{Header:l},template:"<Header/>"}),new a.a({el:"#sidebar",components:{Sidebar:v},template:"<Sidebar/>"}),new a.a({el:"#app",router:S,components:{App:d},template:"<App/>"}),new a.a({el:"#footer",router:S,components:{Footer:u},template:"<Footer/>"})},OTz8:function(e,t){},u22o:function(e,t){}},["NHnr"]);
//# sourceMappingURL=app.346231997cacd0a970b9.js.map