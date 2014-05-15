var App = angular.module('App', ['ngRoute']);

	// configure our routes
	App.config( function ($routeProvider) {
		$routeProvider
			// route for the home page
			.when('/', {
				templateUrl : 'Static/home.html',
				controller  : 'mainController'
			})

			// route for the about page
			.when('/about', {

				templateUrl : 'Static/about.html',
				controller  : 'aboutController'
			})

			// route for the contact page
			.when('/contact', {
				templateUrl : 'Static/contact.html',
				controller  : 'contactController'
			})
            .otherwise({
                redirectTo: '/'
            });
	});

	// create the controller and inject Angular's $scope
	App.controller('mainController', function($scope, $http) {

        $scope.formData = {};
        
        $scope.isitemchecked = function(checked){
            if(checked === true){
                return true;
            }else{return false;}
        };
        
        // when landing on the page, get all todos and show them
        $http.get('/_ah/api/todolist/v1/getlist')
            .success(function(data) {
                $scope.todos = JSON.parse(data.message);
								console.log($scope.todos)
                console.log(data);
            })
            .error(function(data) {
                console.log('Error: ' + data);
            });

        // when submitting the add form, send the text to the node API
        $scope.createTodo = function() {
						console.log({"message" : $scope.formData.title})
            $http.post('/_ah/api/todolist/v1/addItem/', {"message" : $scope.formData.title})
                .success(function(data) {
                    $scope.formData = {}; // clear the form so our user is ready to enter another
                    $scope.todos = JSON.parse(data.message);
                    //{checked:false, title:$scope.formData.title, timestamp:}
                    console.log(data);
                })
                .error(function(data) {
                    console.log('Error: ' + data);
                });
        };

        // check a todo after checking it
        $scope.checkTodo = function(id) {
            $http.post('/_ah/api/todolist/v1/checkItem/' + id)
                .success(function(data) {
                    //$scope.todos = JSON.parse(data.message);
                    console.log(data);
                })
                .error(function(data) {
                    console.log('Error: ' + data);
                });
        };

        // delete a todo after deleting it
        $scope.deleteTodo = function(id) {
            $http.delete('/_ah/api/todolist/v1/removeItem/' + id)
                .success(function(data) {
                    $scope.todos = JSON.parse(data.message);
                    console.log(data);
                })
                .error(function(data) {
                    console.log('Error: ' + data);
                });
        };

	});

	App.controller('aboutController', function($scope) {
		$scope.message = 'Look! I am an about page.';
	});

	App.controller('contactController', function($scope) {
		$scope.message = 'Contact us! JK. This is just a demo.';
	});

//Initialize Smoothscroll
smoothScroll.init();
