import amrlib
import logging

logger = logging.getLogger(__name__)

class ParserFactory():

    def __init__(self):
        return None
	
    def get_parser(self, parser_uri = "t5-amrlib"):

        if parser_uri == "t5-amrlib":
            parser = AMRLibT5()
        elif parser_uri == "gsii-amrlib":
            parser = AMRLibGSII()
        else:
            parser = None
            logger.critical("\"{}\" parser uri not found, \
                    cannot parse anything".format(parser_uri))
        return parser

class AMRLibT5():

    def __init__(self):
        logger.info("Parser loading")
        self.parser = amrlib.load_stog_model(
                model_dir=amrlib.__file__.replace("__init__.py","") 
                + "/data/model_parse_t5-v0_1_0")
        return None
        
    def parse_sents(self, sents):
        graphs = self.parser.parse_sents(sents)
        
        # need check for serialization fails
        for i, g in enumerate(graphs):
            if not g:
                logger.warning("AMR serialization of Seq output failed,\
                        replacing AMR with dummy")
                graphs[i] = "# ::snt " + sents[i] + "\n" + "(er / serialization-error)"
        return graphs

class AMRLibGSII():

    def __init__(self):
        logger.info("Parser loading")
        self.parser = amrlib.load_stog_model(
                model_dir=amrlib.__file__.replace("__init__.py","") 
                + "data/model_parse_gsii-v0_1_0")
        return None
        
    def parse_sents(self, sents):
        graphs = self.parser.parse_sents(sents)
        return graphs
