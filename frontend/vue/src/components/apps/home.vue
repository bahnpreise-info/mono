<template>
    <div class="home">
        <div class="row welcome">
            <div class="col-md-12">
                <h1>BAHNPREISE</h1>
                <h2>Aktuelle und vergangene Ticketpreise anschauen</h2>
            </div>
        </div>
        <div class="btns">
            <a class="btn btn-primary btn-space" href="/#/single_connection" onclick="" role="button">Einzelverbindung suchen
                <i class="fas fa-chevron-circle-right"></i>
            </a>
            <!--<a class="btn btn-primary btn-space" href="#" role="button">Streckenpreise suchen <i class="fas fa-chevron-circle-right"></i></a>-->
        </div>
        <div class="container-fluid">
            <div class="row">
                <!-- Card -->
                <div class="col-xl-4 col-md-4 mb-3">
                    <div class="card border-left-primary shadow h-100 py-2">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Alle Verbindungen</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800" id="totalConnections">{{this.stats.data.connections}}</div>
                                </div>
                                <div class="col-auto">
                                    <i class="fas fa-arrows-alt-h fa-2x text-gray-300"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Card -->
                <div class="col-xl-4 col-md-4 mb-3">
                    <div class="card border-left-primary shadow h-100 py-2">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Aktiv beobachtete Verbindungen</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800" id="activeConnections">{{this.stats.data.activeconnections}}</div>
                                </div>
                                <div class="col-auto">
                                    <i class="fas fa-eye fa-2x text-gray-300"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Card  -->

                <!-- Card -->
                <div class="col-xl-4 col-md-4 mb-3">
                    <div class="card border-left-primary shadow h-100 py-2">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Verfügbare Bahnhöfe</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800" id="stations">{{this.stats.data.stationcount}}</div>
                                </div>
                                <div class="col-auto">
                                    <i class="fas fa-city fa-2x text-gray-300"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Card -->
                <div class="col-xl-4 col-md-4 mb-3">
                    <div class="card border-left-primary shadow h-100 py-2">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Abfragen / Letzte Stunde</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800" id="hourlyRequests">{{this.stats.data.hourlyrequests}}</div>
                                </div>
                                <div class="col-auto">
                                    <i class="fas fa-retweet fa-2x text-gray-300"></i>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Card -->
                <div class="col-xl-4 col-md-4 mb-3">
                    <div class="card border-left-primary shadow h-100 py-2">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Abfragen / Letzte 24 Stunden</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800" id="dailyRequests">{{this.stats.data.dailyrequests}}</div>
                                </div>
                                <div class="col-auto"> <i class="fas fa-arrows-alt-h fa-2x text-gray-300"></i> </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Card -->
                <div class="col-xl-4 col-md-4 mb-3">
                    <div class="card border-left-primary shadow h-100 py-2">
                        <div class="card-body">
                            <div class="row no-gutters align-items-center">
                                <div class="col mr-2">
                                    <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Durchschnittlicher Ticketpreis</div>
                                    <div class="h5 mb-0 font-weight-bold text-gray-800" id="averageCosts">{{this.stats.data.global_average}}€</div>
                                </div>
                                <div class="col-auto"> <i class="fas fa-coins fa-2x text-gray-300"></i> </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <!-- Project Description -->
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">Wie funktioniert das alles?</div>
                <div class="card-body"> Die Daten die hier einsehbar sind werden von einem System permanent direkt von der Website der Bahn abgerufen. Das System gliedert sich in mehrere Teile die im nachfolgenden aufgeschlüsselt sind.
                    <br><small>Zum besseren Verständnis einige Begriffe:<br> Verbindung (Connection): <i>Eine Reiseverbindung von Bahnhof A zu Bahnhof B zu einerm bestimmten Datum und einer bestimmten Uhrzeit. Es können mehrere Züge beinhaltet sein.</i><br> Strecke: <i>Alle Verbindungen auf einer Strecke von Bahnhof A zu Bahnhof B zu beliebiger Uhrzeit und beliebigem Datum.</i><br> Preis/Ticketpreis: <i>Preis einer Verbindung zu einem bestimmten Zeitpunkt. </i> </small>
                    <br> <a class="btn btn-primary btn-space" href="https://github.com/bahnpreise-info/mono" role="button">Code auf GitHub <i class="fas fa-chevron-circle-right"></i></a>
                    <br>
                    <div class="row">
                        <!-- Card -->
                        <div class="col-xl-4 col-md-4 mb-3">
                            <div class="card shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Datenbank</div>
                                            <div class="mb-0">Die Datenbank ist das Herzstück des Systems, hier werden Bahnhöfe, Verbindungen und Preise gespeichert. Es kommt eine MySQL-Datenbank zum Einsatz.</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Card -->
                        <div class="col-xl-4 col-md-4 mb-3">
                            <div class="card shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Connectionmanager</div>
                                            <div class="mb-0">Der Connectionmanager behält den Überblick über die aktiv überwachten Verbindungen. Fällt die Zahl an aktiv überwachten Verbindungen unter eine bestimmte Grenze sucht der Connectionmanager nach neuen Verbindungen. Die Wahl der Bahnhöfe und der Abfahrtszeit geschieht weitgehend zufällig.
                                                <br><small><a href="https://cubicroot.xyz">entwickelt von cubicrootxyz</a></small></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Card -->
                        <div class="col-xl-4 col-md-4 mb-3">
                            <div class="card shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Scheduler </div>
                                            <div class="mb-0">Der Scheduler holt sich immer wieder neue Preise zu den aktiv überwachten Verbindungen. Sind Verbindungen ausgelaufen, also der Zug abgefahren, setzt er die Verbindungen auf inaktiv. Preise werden alle 10-26 Stunden zu zufälligen Zeitpunkten abgefragt, je näher wir dem Abfahrtszeitpunkt kommen umso öfter wird der Preis abgefragt. Die Preise erhält der Scheduler direkt von der Seite der Bahn, dank der <a href="https://github.com/kennell/schiene">Schiene Library</a>.
                                                <br><small><a href="https://cubicroot.xyz">entwickelt von cubicrootxyz</a></small></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Card -->
                        <div class="col-xl-4 col-md-4 mb-3">
                            <div class="card shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">API</div>
                                            <div class="mb-0">Die Inhalte der Datenbank sind über eine JSON-API abrufbar. Die Endpunkte der API bereiten die Daten passend auf.
                                                <br><small><a href="https://stored.cc">entwickelt von storedcc</a></small></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Card -->
                        <div class="col-xl-4 col-md-4 mb-3">
                            <div class="card shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Website</div>
                                            <div class="mb-0">Auf der Website bahnpreise.info sind die Daten graphisch aufbereitet und Nutzer können mit der API interagieren.
                                                <br><small>Funktionalität entwickelt von <a href="https://storedcc">storedcc</a>, Design entwickelt von <a href="https://cubicroot.xyz">cubicrootxyz</a></small></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- Card -->
                        <div class="col-xl-4 col-md-4 mb-3">
                            <div class="card shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">CSV-Download</div>
                                            <div class="mb-0">Noch in Arbeit...</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- End of Project Description -->
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name: 'home',
    methods: {
        updateStats(){
            axios.get(this.apiUrl + '/stats').then(response => {
                console.log(response.data);
                this.stats = response.data;
            });
        },
    },
    data () {
    return {
        stats: {
            "data": {
                "activeconnections": 0,
                "stationcount": 0,
                "hourlyrequests": 0,
                "connections": 0,
                "dailyrequests": 0,
                "globalaverageprice": 0
            }
        },
    }
    },
    mounted() {
        this.updateStats();
    }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
