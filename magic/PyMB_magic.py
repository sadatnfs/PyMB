def import_pymb_magic():
    # so many imports
    from IPython.core.magic import (magics_class, Magics, cell_magic, line_magic, MagicsManager)
    from IPython.core.magic_arguments import (argument, kwds, magic_arguments, parse_argstring)
    from IPython.core.display import display_javascript
    import PyMB

    # turn on C++ highlighting for PyMB cells
    display_javascript("IPython.config.cell_magic_highlight['magic_clike'] = {'reg':[/^%%PyMB/]};", raw=True)

    # define PyMB magic class
    @magics_class
    class PyMBMagics(Magics):
        """A PyMB magic for writing a model in .
        """

        def __init__(self, shell):
            """
            Parameters
            ----------

            shell : IPython shell

            """
            super(PyMBMagics, self).__init__(shell)

        @magic_arguments()
        @argument('name', type=str,
                  help='The model name. A new model object will be created using this name.')
        @argument('-TMB', '--TMB_DIR', type=str, default='/usr/local/lib/R/site-library/TMB/include',
                  help='''TMB_DIR : str, default '/usr/local/lib/R/site-library/TMB/include'
                        location of TMB library''')
        @argument('-R', '--R_DIR', type=str, default='/usr/share/R/include',
                  help='''R_DIR : str, default '/usr/share/R/include'
                        location of R shared library
                        Note: R must be built with shared libraries
                        See http://stackoverflow.com/a/13224980/1028347''')
        @argument('-CC', '--CCOMPILER', type=str, default='g++',
                  help='''CCOMPILER : str, default 'g++'
                        C++ compiler to use''')
        @argument('-OUT', '--OUTPUT_DIR', type=str, default='tmb_tmp',
                  help='''OUTPUT_DIR : str, default 'tmb_tmp'
                        output directory for .cpp and .o files''')
        @argument('-I', '--INCLUDE', type=list, default=['TMB.hpp'],
                  help='''INCLUDE : list, default ['TMB.hpp']
                        other libraries to include''')
        @argument('-U', '--USING', type=list, default=['namespace density'],
                  help='''USING: list, default ['namespace density']
                        namespaces, libraries, etc to include, e.g. Eigen::SparseMatrix''')
        @argument('-V', '--VERBOSE', type=bool, default=False,
                  help='''VERBOSE: boolean, default False
                          prints model code to be compiled''')
        @cell_magic
        def PyMB(self, line, cell):
            # parse arguments
            args = parse_argstring(self.PyMB, line)
            name = args.name
            #opts = args.opts

            # make a new model
            model = PyMB.model(name=name)
            self.shell.push({name: model})
            print('Created model {}.'.format(name))

            # create code string
            code = ''

            # add includes
            for i in args.INCLUDE:
                code += '#include <{}>\n'.format(i)

            # add using
            for u in args.USING:
                code += 'using {};\n'.format(u)

            # add template
            code += 'template<class Type>\n'

            # start objective function
            code += '\nType objective_function<Type>::operator() () {\n'

            # add cell contents (with tab indenting to make it look nicer)
            code += '\n'.join(['    ' + c for c in cell.split('\n')]) + '\n'

            # close objective function
            code += '}\n'

            # compile model
            model.compile(codestr=code, output_dir=args.OUTPUT_DIR, cc=args.CCOMPILER, R=args.R_DIR, TMB=args.TMB_DIR)

            # print if verbose
            if args.VERBOSE == True:
                print('Code:\n\n{}'.format(code))

    ip = get_ipython()
    ip.register_magics(PyMBMagics)