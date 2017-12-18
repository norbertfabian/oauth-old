(function (gulp) {
    'use strict';

    const config = {
        copy: {
            src: './vendor/components-font-awesome/fonts/**',
            output: './oauth/static/fonts/'
        },
        js: {
            src: './js/**/*.js',
            sourcemaps: true,
            output: {
                file: 'site.js',
                path: './oauth/static/'
            },
            tpl: './oauth/static/templateCache.js',
            vendor: [
                './vendor/angular/angular.js',
                './vendor/angular-sanitize/angular-sanitize.js',
                './vendor/angular-resource/angular-resource.js',
                './vendor/angular-route/angular-route.js',
                './vendor/angular-ui-router/release/angular-ui-router.js',
                './vendor/angular-local-storage/dist/angular-local-storage.js'
            ],
            watch: true
        },
        sass: {
            src: './style/index.scss',
            sourcemaps: false,
            output: {
                file: 'site.css',
                path: './oauth/static/'
            },
            options: {
                includePaths : [
                    './style/',
                    './vendor/'
                ]
            },
            watch: './style/**/*.scss'
        },
        tpl: {
            src: './js/**/*.tpl.html',
            output: {
                file: 'templateCache.js',
                path: './oauth/static/'
            },
            watch: true
        }
    };

    gulp(config);

}(function (path, gulp, gutil, concat, cssnano, plumber, sass, sourcemaps, autoprefix, changed,
                rename, babel, ngAnnotate, uglify, jshint, stylish, addsrc, insert, htmlMin, ngHtml2js) {
    'use strict';

    return output;

    function output(config)
    {
        taskCopy.description = "Copy static files";
        taskSass.description = "Compile SASS files";
        taskWatch.description = "Watch file changes";
        taskJS.description = "Compile JS files";

        gulp
            .task('copy', [], taskCopy)
            .task('sass', [], taskSass)
            .task('tpl', [], taskTpl)
            .task('jshint', [], taskJSHint)
            .task('js', [ 'jshint', 'tpl' ], taskJS)
            .task('default', [ 'copy', 'sass', 'js' ], (done) => { done(); })
            .task('watch', taskWatch);

        function taskJS()
        {
            const sm = !!config.js.sourcemaps
                ? sourcemaps
                : { init: gutil.noop, write: gutil.noop };

            return gulp.src(config.js.src, { base: './' })
                       .pipe(plumber(taskErrorFactory('js', false)))
                       .pipe(sm.init())
                       .pipe(babel())
                       .pipe(ngAnnotate({
                            add: true,
                            single_quotes: true
                        }))
                       .pipe(addsrc.prepend(config.js.tpl))
                       .pipe(addsrc.prepend(config.js.vendor))
                       .pipe(concat(config.js.output.file))
                       .pipe(gulp.dest(config.js.output.path))
                       .pipe(uglify({ preserveComments: false }))
                       .pipe(rename((path) => { path.basename += '.min'; }))
                       .pipe(sm.write())
                       .pipe(gulp.dest(config.js.output.path))
                       .on('end', () => { gutil.log(gutil.colors.green("JS Compiled")); });
        }

        function taskJSHint()
        {
            gutil.log('runing jshint...');

            return gulp.src(config.js.src)
                       .pipe(jshint({ esversion: 6 }))
                       .pipe(jshint.reporter(stylish))
                       .on('end', () => { gutil.log(gutil.colors.green("JSHint finished")); });
        }

        function taskCopy(done)
        {
            if (Array.isArray(config.copy))
            {
                let promises = [];
                for (let i = 0; i < config.copy.length; i++)
                {
                    promises.push(new Promise((res) => { execute(config.copy[i]).on('end', res); }));
                }
                Promise.all(promises).then(success);
            }
            else execute(config.copy).on('end', success);

            function execute(conf)
            {
                return gulp.src(conf.src)
                           .pipe(plumber(taskErrorFactory('copy', false)))
                           .pipe(gulp.dest(conf.output));
            }

            function success()
            {
                gutil.log(gutil.colors.green("Static files coppied"));
                done();
            }

        }

        function taskSass()
        {
            const sm = !!config.sass.sourcemaps
                ? sourcemaps
                : { init: gutil.noop, write: gutil.noop };

            return gulp.src(config.sass.src)
                       .pipe(plumber(taskErrorFactory('sass', false)))
                       .pipe(sm.init())
                       .pipe(sass(config.sass.options))
                       .pipe(autoprefix())
                       .pipe(concat(config.sass.output.file))
                       .pipe(cssnano())
                       .pipe(sm.write())
                       .pipe(gulp.dest(config.sass.output.path))
                       .on('end', () => { gutil.log(gutil.colors.green("SASS compiled")); });
        }

        function taskTpl()
        {
            const RENAME_PATTERN = /^(ng|js|modules?|tpl|templates?|components?|directives?|views?)$/i;
            const NG_MODULE = 'templateCache';

            return gulp.src(config.tpl.src)
                       .pipe(plumber(taskErrorFactory('tpl', true)))
                       .pipe(htmlMin({ collapseWhitespace: true }))
                       .pipe(rename((p) => {
                           let dir = p.dirname.split(path.sep);
                           let newDir = [];

                           for (let i = 0; i < dir.length; i++)
                           {
                               if (!RENAME_PATTERN.test(dir[i])) newDir.push(dir[i]);
                           }
                           p.dirname = newDir.join(path.sep);
                           p.extname = '';
                       }))
                       .pipe(ngHtml2js({
                           moduleName: NG_MODULE,
                           declareModule: false
                       }))
                       .pipe(concat(config.tpl.output.file))
                       .pipe(insert.prepend(`
                            (function (angular) {
                                angular.module('${NG_MODULE}', []);
                        `))
                       .pipe(insert.append("\n\n}(angular));"))
                       .pipe(gulp.dest(config.tpl.output.path))
                       .on('end', () => { gutil.log(gutil.colors.green("Template cache compiled")); });
        }

        function taskWatch()
        {
            if (config.sass.watch)
            {
                gulp.watch(config.sass.watch, [ 'sass' ]);
                gutil.log(gutil.colors.cyan("Watching SASS files..."));
            }

            if (config.js.watch)
            {
                let src = config.js.watch === true
                    ? config.js.src
                    : config.js.watch;

                gulp.watch(src, [ 'jshint', 'js' ]);
                gutil.log(gutil.colors.cyan("Watching JS files..."));
            }

            if (config.tpl.watch)
            {
                let src = config.tpl.watch === true
                    ? config.tpl.src
                    : config.tpl.watch;

                gulp.watch(src, [ 'js' ]);
                gutil.log(gutil.colors.cyan("Watching TemplateCache files..."));
            }
        }

        function taskErrorFactory(plugin, stack)
        {
            return TaskError;

            function TaskError(msg)
            {
                let err = new gutil.PluginError(plugin, {
                    message: msg || '',
                    showStack: !!stack
                });

                console.error(err.toString());

                this.emit('end');
            }
        }
    }
}(
    require('path'),
    require('gulp'),
    require('gulp-util'),
    require('gulp-concat'),
    require('gulp-cssnano'),
    require('gulp-plumber'),
    require('gulp-sass'),
    require('gulp-sourcemaps'),
    require('gulp-autoprefixer'),
    require('gulp-changed'),
    require('gulp-rename'),
    require('gulp-babel'),
    require('gulp-ng-annotate'),
    require('gulp-uglify'),
    require('gulp-jshint'),
    require('jshint-stylish'),
    require('gulp-add-src'),
    require('gulp-insert'),
    require('gulp-htmlmin'),
    require('gulp-ng-html2js')
)));
