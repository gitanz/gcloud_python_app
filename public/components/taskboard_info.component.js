angular.
  module('TaskManagementApp').
  component('taskboardInfo', {
    templateUrl: '/templates/taskboard_info.html',
    controller: function TaskboardController($scope, $rootScope, $http, $location, $routeParams) {
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
                url: base_url+"/taskboards/"+$scope.taskboardId+"/tasks"
            }).then(function successCallback(response){
                if(response.data.success){
                    $scope.tasks = response.data.data
                }else{
                    $scope.tasks.errors = response.data.errors
                }
            })

            // get members
            $http({
                method:"GET",
                url: base_url+"/taskboard_members/"+$scope.taskboardId
            }).then(function successCallback(response){
                if(response.data.success){
                    $scope.taskboard.members = response.data.data;
                }else{
                    $scope.taskboard.members = {}
                    $scope.taskboard.members.errors = response.data.errors
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

        $scope.showTaskModal = function(title, submitValue, height='400', width='400', task_id=false, readonly=false){
            $scope.addTaskModal = true
            $scope.taskModal.save = submitValue
            $scope.taskModal.title = title
            $scope.taskModal.height = height+'px'
            $scope.taskModal.width = width+'px'
            $scope.taskModal.contentHeight = (height-50)+'px'
            $scope.taskModal.editModal = false
            $scope.taskModal.readonly = readonly
            console.log($scope.taskModal.readonly)
            if(task_id){
                $scope.taskModal.editModal = true
                $http({
                    url: base_url+'/tasks/'+task_id,
                    method: 'get',
                }).then(function successCallback(response){
                    if(response.data.success){
                        $scope.task.isEdit = true
                        $scope.task = response.data.data
                        $scope.task.due_date = new Date($scope.task.due_date)
                        $scope.task.status = $scope.task.status ? "1":"0"
                        console.log($scope.task.status)
                    }
                })
            }
        }

        $scope.closeTaskModal = function(){
            $scope.addTaskModal = false
            $scope.task = {}
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
                    $scope.fetchData()
                    $scope.errors = {}
                    $scope.taskboardUser = {}
                    $scope.addMemberModal = false
                }else{
                    $scope.errors = response.data.errors
                }
            })
        }

        $scope.memberDelete = function(member){
            $rootScope.confirmModal = {
                showModal: true,
                modalTitle: 'Delete Member',
                modalText: 'Are you sure you want to delete this member. All the tasks assigned to this member will be unassigned.',
                contentHeight: '150px',
                height: '200px',
                width: '350px',
                successButton: 'Ok',
                cancelButton: 'Cancel',
                confirmCallback: function(){
                    $http({
                        url:base_url+'/taskboard_members/delete',
                        method: 'POST',
                        data: member
                    }).then(function successCallback(response){
                        if(response.data.success){
                            $rootScope.confirmModal = {}
                            $scope.fetchData()
                        }else{
                            $rootScope.errors = response.data.errors
                        }
                    })
                },
                cancelCallback: function(){
                    $rootScope.confirmModal = {}
                }
            }

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

        $scope.markTaskComplete = function(task){

            $rootScope.confirmModal = {
                    showModal: true,
                    modalTitle: 'Mark as Completed',
                    modalText: 'Are you sure you want to mark this task as Completed ?',
                    contentHeight: '150px',
                    height: '200px',
                    width: '350px',
                    successButton: 'Yes',
                    cancelButton: 'Cancel',
                    confirmCallback: function(){
                        $http({
                            url: base_url+'/tasks/'+task.id+"/mark-complete",
                            method: 'POST',
                            data: {'id': task.id}
                        }).then(function successCallback(response){
                            if(response.data.success){
                                $scope.fetchData()
                                $scope.fetchData()
                            }else{
                                $scope.errors = response.data.errors
                            }
                            $rootScope.confirmModal = {}
                        })
                    },
                    cancelCallback: function(){
                        $rootScope.confirmModal = {}
                    }
                }


        }

        $scope.markTaskOngoing = function(task){

            $rootScope.confirmModal = {
                    showModal: true,
                    modalTitle: 'Mark as On-going',
                    modalText: 'Are you sure you want to mark this task as On-going ?. Previous completion date CANNOT be recovered.',
                    contentHeight: '150px',
                    height: '200px',
                    width: '350px',
                    successButton: 'Yes',
                    cancelButton: 'Cancel',
                    confirmCallback: function(){
                        $http({
                            url: base_url+'/tasks/'+task.id+"/mark-ongoing",
                            method: 'POST',
                            data: {'id': task.id}
                        }).then(function successCallback(response){
                            if(response.data.success){
                                $scope.fetchData()
                                $scope.fetchData()
                            }else{
                                $scope.errors = response.data.errors
                            }
                            $rootScope.confirmModal = {}
                        })
                    },
                    cancelCallback: function(){
                        $rootScope.confirmModal = {}
                    }
                }
        }

        $scope.deleteTask = function(task){

            $rootScope.confirmModal = {
                showModal: true,
                modalTitle: 'Delete Task',
                modalText: 'Are you sure you want to delete this task ? Deleted task\'s CANNOT be recovered again.',
                contentHeight: '150px',
                height: '200px',
                width: '350px',
                successButton: 'Yes',
                cancelButton: 'Cancel',
                confirmCallback: function(){
                    $http({
                        url: base_url+'/tasks/'+task.id+"/delete",
                        method: 'POST',
                        data: {'id': task.id}
                    }).then(function successCallback(response){
                        if(response.data.success){
                            $scope.fetchData()
                            $scope.fetchData()
                        }else{
                            $scope.errors = response.data.errors
                        }
                        $rootScope.confirmModal = {}

                    })
                },
                cancelCallback: function(){
                    $rootScope.confirmModal = {}
                }
            }
        }
    }
  })