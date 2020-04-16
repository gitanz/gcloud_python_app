angular.
  module('TaskManagementApp').
  component('taskboardInfo', {
    templateUrl: '/templates/taskboard_info.html',
    controller: function TaskboardController($scope, $http, $location, $routeParams) {
        self = this;
        $scope.taskboardId = $routeParams.taskboardId
        // on initialization
        $scope.fetchData = function(){
            $http({
                method:"GET",
                url: base_url+"/taskboards/"+$scope.taskboardId
            }).then(function successCallback(response){
                $scope.taskboard.title = response.data.data.title
                $scope.taskboard.created_date = response.data.data.created_date
                $scope.taskboard.created_by = response.data.data.created_by
                $scope.taskboard.creator = response.data.data.creator
                $scope.taskboard.updated_date = response.data.data.updated_date

            },function errorCallback(response){

            })
        }
        this.$onInit = function(){
            $scope.taskboard = {}
            $scope.fetchData()
        }
    }
  })