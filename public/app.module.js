'use strict';

var App = angular.module('TaskManagementApp', [
'ngRoute'
]);

App.factory('myModal', function($http, $q) {

    var myModal = {showMyModal: false, title:"", content:""}

    myModal.open = function(title, contentUrl, width, height){
        myModal.title = title;
        var deferred = $q.defer();
        $http.get(contentUrl).then(function(response) {
             myModal.content = response.data;
             myModal.height = height;
             myModal.width = width;
             angular.element(document.querySelector('#myOverlay')).css("display", "block")
             myModal.showMyModal = true;
             deferred.resolve();
        });
        return deferred.promise
    }

    myModal.close = function(){
        angular.element(document.querySelector('#myOverlay')).css("display", "none")
        myModal.showMyModal = false;
    }

    return myModal;
});

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
  $routeProvider.otherwise({
    redirectTo : '/'
  });
});
