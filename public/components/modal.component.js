angular.
  module('TaskManagementApp').
  component('addTaskboard', {
    templateUrl: '/templates/addTaskboard.html',
    controller: function AddTaskboardController($element, myModal, $scope, $sce) {
        $scope.title = myModal.title;
        $scope.content = myModal.content;
        $scope.height = myModal.height;
        $scope.width = myModal.width;
        this.closeModal = function(){
            var event = new CustomEvent('closemodal');
            $element[0].dispatchEvent(event)
        }
    }
  });