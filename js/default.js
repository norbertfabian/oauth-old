(function () {
    'use strict';

    angular
        .module('default', [
            'ngInject',
            'ui.router'
        ])
        .config(config)
        ;

    function config($stateProvider)
    {
        $stateProvider.state('oauth.default', {
            url: '/',
            views: {
                'main@': {
                    templateUrl: 'default.tpl'
                }
            }

        });
    }
}());
