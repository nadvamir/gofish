module.exports = (grunt) ->

  fs = require 'fs'
  isModified = (filepath) ->
    now = new Date()
    modified =  fs.statSync(filepath).mtime
    return (now - modified) < 10000

  grunt.initConfig

    coffee:
      options:
        sourceMap: true
        bare: true
        force: true # needs to be added to the plugin
      all:
        expand: true
        cwd: 'static/src/'
        src: '*.coffee'
        dest: 'static/js'
        ext: '.js'
      modified:
        expand: true
        cwd: 'static/src/'
        src: '*.coffee'
        dest: 'static/js'
        ext: '.js'
        filter: isModified

    watch:
      coffeescript:
        files: ['static/src/*.coffee']
        tasks: ['coffee:modified']

  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-watch'

  grunt.registerTask 'default', ['coffee:all', 'watch']

