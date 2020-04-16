'use strict';

var App = angular.module('TaskManagementApp', [
'ngRoute'
]);

App.filter('rawHtml', ['$sce', function($sce){
  return function(val) {
    return $sce.trustAsHtml(val);
  };
}]);

App.config(function($routeProvider) {
  $routeProvider.when('/dashboard', {
    template: '<dashboard></dashboard>',
  });
  $routeProvider.when('/taskboards', {
    template: '<taskboard></taskboard>',
  });
  $routeProvider.when('/taskboard/:taskboardId', {
    template: '<taskboard-info></taskboard-info>',
  });
  $routeProvider.otherwise({
    redirectTo : '/'
  });
});
