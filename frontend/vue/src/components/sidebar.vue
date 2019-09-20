<template>
    <div id="sidebar" style="background: #d10e0e;">
        <ul class="navbar-nav bg-gradient-primary sidebar toggled sidebar-dark accordion ml-xl-auto" id="accordionSidebar">

            <!-- Sidebar - Brand -->
            <a class="sidebar-brand d-flex align-items-center justify-content-center" href="/#/">
                <div class="sidebar-brand-icon">
                    <i class="fas fa-subway"></i>
                </div>
                <div class="sidebar-brand-text mx-2">Bahnpreise.info</div>
            </a>

            <!-- Divider -->
            <hr class="sidebar-divider my-0">

            <!-- Nav Item - Dashboard -->
            <li class="nav-item">
                <a class="nav-link" href="/#/">
                    <i class="fas fa-fw fa-home"></i>
                    <span>Home</span></a>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider">

            <!-- Heading -->
            <div class="sidebar-heading">
                Abfragen
            </div>

            <li class="nav-item">
                <a class="nav-link" href="/#/single_connection">
                    <i class="fas fa-fw fa-long-arrow-alt-right"></i>
                    <span>Einzelverbindung</span></a>
            </li>

            <li class="nav-item">
                <a class="nav-link">
                    <i class="fas fa-fw fa-arrows-alt-h"></i>
                    <span>Strecken (kommt bald)</span></a>
            </li>

            <li class="nav-item">
                <a class="nav-link">
                    <i class="fas fa-fw fa-arrows-alt"></i>
                    <span>Statistik (kommt bald)</span></a>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider">

            <!-- Heading -->
            <div class="sidebar-heading">
                Sonstiges
            </div>

            <li class="nav-item">
                <a class="nav-link" href="/#/faq">
                    <i class="fas fa-fw fa-question-circle"></i>
                    <span>FAQ</span></a>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider d-none d-md-block">

            <!-- Sidebar Toggler (Sidebar) -->
            <div class="text-center d-none d-md-inline">
                <button class="rounded-circle border-0" id="sidebarToggle"></button>
            </div>

        </ul>
    </div>
</template>
<script>
export default {
  name: 'sidebar'
}
</script>
