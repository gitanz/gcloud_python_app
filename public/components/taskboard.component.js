angular.
  module('TaskManagementApp').
  component('taskboard', {
    templateUrl: '/templates/taskboard.html',
    controller: function TaskboardController($scope, $http, $location) {
        self = this;
        // on initialization
        $scope.fetchData = function(){
            $http({
                    method:"GET",
                    url: base_url+"/taskboards",
                }).then(function successCallback(response){
                    if(response.data.success){
                        $scope.taskboardData = response.data.data
                    }
                })
        }
        this.$onInit = function(){
            $scope.taskboard = {};
            $scope.taskboardData = [];
            $scope.fetchData();
            $scope.displayModal = false;
            $scope.errors = {}
        }
        // handler for add board button
        $scope.addTaskboard = function(title, contentUrl, width, height){
            $scope.title = title
            $scope.displayModal = true;
            $scope.height = height;
            $scope.width = width;
        }
        $scope.editTaskboard = function(title, contentUrl, width, height, taskboardId){
            $http({
                method:"GET",
                url: base_url+"/taskboards/"+taskboardId
            }).then(function successCallback(response){
                if(response.data.success){
                    $scope.title = title
                    $scope.displayModal = true;
                    $scope.height = height;
                    $scope.width = width;
                    $scope.taskboard = response.data.data
                }else{

                }
            },function errorCallback(response){

            })
        }
        // handler for modal close button
        $scope.closeTaskboard = function($event) {
            $scope.displayModal = false;
            $scope.taskboard = {}
            $scope.errors = {}
        }
        // handler for add form modal save
        $scope.saveTaskboard = function(){
        // send http req to save taskboard
        // show in table
            $http({
                method:"POST",
                url: base_url+"/taskboards",
                data: $scope.taskboard
            }).then(function successCallback(response){
                if(response.data.success){
                    $scope.success = response.data.success
                    $scope.message = response.data.message
                    $scope.fetchData()
                    $scope.taskboard = {}
                    $scope.displayModal = false;
                }else{
                    $scope.errors = response.data.errors
                }
            },function errorCallback(response){

            })
        }

        $scope.showTaskboard = function(taskboardId){
            $location.path('/taskboard/'+taskboardId)
        }
    }
  })