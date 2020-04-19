angular.
  module('TaskManagementApp').
  component('sideBar', {
    templateUrl: '/templates/sidebar.html',
    controller: function SidebarController() {

      this.navs = [
        {
            "text": "Taskboards",
            "link": "#!/taskboards",
            "icon": "project-diagram"
        }
      ]
    }
  });