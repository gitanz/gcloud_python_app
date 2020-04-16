angular.
  module('TaskManagementApp').
  component('sideBar', {
    templateUrl: '/templates/sidebar.html',
    controller: function SidebarController() {
      this.navs = [
        {
            "text": "Dashboards",
            "link": "#!/dashboard",
            "icon": "chart-line"
        },
        {
            "text": "Taskboards",
            "link": "#!/taskboards",
            "icon": "project-diagram"
        },
        {
            "text": "Tasks",
            "link": "#!/tasks",
            "icon": "tasks"
        },
        {
            "text": "Users",
            "link": "#!/users",
            "icon": "users"
        }
      ]
    }
  });