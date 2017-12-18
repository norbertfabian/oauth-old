
                            (function (angular) {
                                angular.module('templateCache', []);
                        angular.module('templateCache').run(['$templateCache', function($templateCache) {
  $templateCache.put('default.tpl',
    '<h1>Přihlášeno</h1><p><i class="fa fa-5x fa-check color-primary" aria-hidden="true"></i></p>');
}]);


}(angular));