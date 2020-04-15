angular.
  module('TaskManagementApp').
  component('.taskboardForm', {
    templateUrl: '/templates/add_board.html',
    controller: function TaskboardFormController($element, myModal, $scope, $sce) {
        $scope.title = myModal.title;
        $scope.content = myModal.content;
        $scope.height = myModal.height;
        $scope.width = myModal.width;
    }
  });