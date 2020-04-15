angular.
  module('TaskManagementApp').
  component('taskboard', {
    templateUrl: '/templates/taskboard.html',
    controller: function TaskboardController($scope, myModal, $http) {
        self = this;
        // on initialization
        this.$onInit = function(){
            $scope.taskboard = {}
            $scope.taskboardData = []
            $http({
                method:"GET",
                url: base_url+"/taskboards",
                data: {'offset':0, 'limit':20}
            }).then(function successCallback(response){
                if(response.data.success){
                    $scope.taskboardData = response.data.data
                    console.log($scope.taskboardData)
                }else{

                }
            },function errorCallback(response){

            })
            $scope.displayModal = false;
        }
        // handler for add board button
        $scope.addTaskboard = function(title, contentUrl, width, height){
            $scope.title = title
            $scope.displayModal = true;
            $scope.height = height;
            $scope.width = width;
        }
        // handler for modal close button
        $scope.closeTaskboard = function($event) {
            $scope.displayModal = false;
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
                    $scope.taskboardData.push(response.data.data)
                    $scope.taskboard = {}
                    $scope.displayModal = false;
                }else{
                }
            },function errorCallback(response){

            })
        }
    }
  })