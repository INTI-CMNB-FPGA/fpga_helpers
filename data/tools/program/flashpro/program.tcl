open_project -file {libero-soc/libero-soc.prjx}
run_tool -name {CONFIGURE_CHAIN} -script {libero-soc/flashpro5.tcl}
run_tool -name {PROGRAMDEVICE}
