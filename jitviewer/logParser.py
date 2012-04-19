
def main():
    if not '__pypy__' in sys.builtin_module_names:
        print "Please run it using pypy-c"
        sys.exit(1)
    #
    server_mode = True
    if '--qt' in sys.argv:
        server_mode = False
        sys.argv.remove('--qt')
    #
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print __doc__
        sys.exit(1)
    filename = sys.argv[1]
    extra_path = os.path.dirname(filename)
    if len(sys.argv) != 3:
        port = 5000
    else:
        port = int(sys.argv[2])
    storage = LoopStorage(extra_path)
    log, loops = import_log(filename, ParserWithHtmlRepr)
    parse_log_counts(extract_category(log, 'jit-backend-count'), loops)
    storage.loops = [loop for loop in loops
                     if not loop.descr.startswith('bridge')]
    storage.loop_dict = create_loop_dict(loops)
    print loops,log,storage
    app = OverrideFlask('_jitviewer')
    server = Server(filename, storage)
    app.debug = True
    app.route('/')(server.index)
    app.route('/loop')(server.loop)
    def run():
        app.run(use_reloader=False, host='0.0.0.0', port=port)

    if server_mode:
        run()
    else:
        url = "http://localhost:%d/" % port
        run_server_and_browser(app, run, url, filename)
