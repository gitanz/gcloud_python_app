'use strict';

var App = angular.module('TaskManagementApp', [
'ngRoute'
]);

App.filter('rawHtml', ['$sce', function($sce, $rootScope){
  return function(val) {
    return $sce.trustAsHtml(val);
  };
}]);

App.run(function($rootScope) {
  $rootScope.confirmModal = {
    showModal: false,
    modalTitle: '',
    modalText: '',
    contentHeight:'200px',
    successButton:'Ok',
    cancelButton:'Cancel',
    confirmCallback: function(){},
    cancelCallback: function(){}
}

});

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
