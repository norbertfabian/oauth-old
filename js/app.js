(function () {
    'use strict';

    angular
        .module('oauth', [
            'ngInject',
            'ngSanitize',
            'ngResource',
            'LocalStorageModule',
            'ui.router',
            // private modules
            'templateCache',
            'default'
        ])
        .constant('app', {
            name: 'oAuth',
            debugMode: true
        })
        .config(config)
        .value('pageData', {
            title: 'oAuth'
        })
        .controller('MainCtrl', MainCtrl)
        .run(appRun)
        ;

    function config($logProvider, $httpProvider, $resourceProvider, $urlRouterProvider,
                        $compileProvider, $stateProvider, localStorageServiceProvider, app)
    {
        $logProvider.debugEnabled(app.debugMode);

        $httpProvider.useApplyAsync(true);

        $resourceProvider.defaults.stripTrailingSlashes = false;

        $urlRouterProvider.otherwise('/');

        $compileProvider.debugInfoEnabled(false);

        $stateProvider.state('oauth', {
            abstract: true
        });

        localStorageServiceProvider.setPrefix(app.name);
    }

    function appRun($window, $rootScope, $log, $state, app)
    {
        // disable logs if not in debug mode
        if (!app.debugMode) {
            $log.info = angular.noop;
            $log.error = angular.noop;
            $log.warn = angular.noop;
        }

        // extending $state by $from parameter
        $rootScope.$on('$stateChangeSuccess', (event, toState, toParams, fromState, fromParams) => {
            let extender = { $from: fromState };
            extender.$from.params = fromParams;
            angular.extend($state, extender);

            $log.info("Current state:", toState.name);
        });

        // disable standard error logs
        $window.onerror = angular.noop;
    }

    function MainCtrl($rootScope, pageData)
    {
        $rootScope.page = pageData;
    }

    angular.module('ngInject', []);
}());
