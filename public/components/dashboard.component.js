angular.
  module('TaskManagementApp').
  component('dashboard', {
    templateUrl: '/templates/dashboards.html',
    controller: function DashboardController() {
        console.log(arguments)
    }
  });