angular.
  module('TaskManagementApp').
  component('sideBar', {
    templateUrl: '/templates/sidebar.html',
    controller: function SidebarController() {
      this.navs = [
        {
            "text": "Dashboards",
            "link": "#!/dashboard"
        },
        {
            "text": "Taskboards",
            "link": "#!/taskboards"
        },
        {
            "text": "Tasks",
            "link": "#!/tasks"
        },
        {
            "text": "Users",
            "link": "#!/users"
        }
      ]
    }
  });