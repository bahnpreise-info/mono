<template>
<!-- Topbar -->
<nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">
    <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3" v-on:click="togglesidebar">
        <i class="fa fa-bars"></i> Menu
    </button>
    <div id="header"></div>
    {{this.sitename}}
</nav>
<!-- End of Topbar -->
</template>

<script>
    const title = 'Bahnpreise.info';
    export default {
        methods: {
            togglesidebar: function () {
                $("body").toggleClass("sidebar-toggled");
                $(".sidebar").toggleClass("toggled");
                if ($(".sidebar").hasClass("toggled")) {
                    $('.sidebar .collapse').collapse('hide');
                }
            }
        }
    }
</script>
