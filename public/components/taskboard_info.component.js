angular.
  module('TaskManagementApp').
  component('taskboardInfo', {
    templateUrl: '/templates/taskboard_info.html',
    controller: function TaskboardController($scope, $http, $location, $routeParams) {
        self = this;
        $scope.taskboardId = $routeParams.taskboardId

        this.$onInit = function(){
            $scope.taskboard = {}
            $scope.tasks = []
            $scope.users = []
            $scope.members = []
            $scope.task = {}
            $scope.addTaskModal = false
            $scope.addMemberModal = false
            $scope.taskModal = {}
            $scope.memberModal = {}
            $scope.taskboardUser = {}
            $scope.errors = {}
            $scope.fetchData()
        }
        $scope.fetchData = function(){
            // get taskboard
            $http({
                method:"GET",
                url: base_url+"/taskboards/"+$scope.taskboardId
            }).then(function successCallback(response){
                $scope.taskboard.id = response.data.data.id
                $scope.taskboard.title = response.data.data.title
                $scope.taskboard.created_date = response.data.data.created_date
                $scope.taskboard.created_by = response.data.data.created_by
                $scope.taskboard.creator = response.data.data.creator
                $scope.taskboard.updated_date = response.data.data.updated_date
                $scope.taskboardUser.taskboard = $scope.taskboard.id
                $scope.task.taskboard_id = $scope.taskboard.id
            })

            $http({
                method:"GET",
                url: base_url+"/tasks/"+$scope.taskboardId
            }).then(function successCallback(response){
                console.log(response)
            })

            // get members
            $http({
                method:"GET",
                url: base_url+"/taskboard_members/"+$scope.taskboardId
            }).then(function successCallback(response){
                if(response.data.success){
                    $scope.taskboard.members = response.data.data;
                }
            })

            // get users
            $http({
                method:"GET",
                url: base_url+"/app_users"
            }).then(function successCallback(response){
                if(response.data.success){
                    $scope.users = response.data.data
                }
            })
        }

        $scope.showTaskModal = function(title, submitValue, height='400', width='400'){
            $scope.addTaskModal = true
            $scope.taskModal.save = submitValue
            $scope.taskModal.title = title
            $scope.taskModal.height = height+'px'
            $scope.taskModal.width = width+'px'
            $scope.taskModal.contentHeight = (height-50)+'px'
        }

        $scope.closeTaskModal = function(){
            $scope.addTaskModal = false
        }

        $scope.showMemberModal = function(title, submitValue, height='400', width='400'){
            $scope.addMemberModal = true
            $scope.memberModal.save = submitValue
            $scope.memberModal.title = title
            $scope.memberModal.height = height+'px'
            $scope.memberModal.width = width+'px'
            $scope.memberModal.contentHeight = (height-50)+'px'
        }

        $scope.closeMemberModal = function(){
            $scope.addMemberModal = false
        }

        $scope.saveMemberToTaskboard = function(){
            $http({
                url: base_url+'/taskboard_members',
                method: 'POST',
                data: $scope.taskboardUser
            }).then(function successCallback(response){
                if(response.data.success){
                    $scope.fetchData()
                    $scope.errors = {}
                    $scope.taskboardUser = {}
                    $scope.addMemberModal = false
                }else{
                    $scope.errors = response.data.errors
                }
            })
        }

        $scope.saveTaskToTaskboard = function(){
            $http({
                url: base_url+'/tasks',
                method: 'POST',
                data: $scope.task
            }).then(function successCallback(response){
                if(response.data.success){
                    $scope.fetchData()
                    $scope.errors = {}
                    $scope.task = {}
                    $scope.addTaskModal = false
                }else{
                    $scope.errors = response.data.errors
                }
            })
        }
    }
  })