from flask_restful import reqparse , abort
from .xlsx_actions import XLSXData
class NovelParser():
    """
    define different parser for different http methods 
    """  
    

    @staticmethod
    def export_post_parser():
        """
        define parser for create new row for specfic novel
        ensure request body include arguments
        """
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('writer',type=str,required=True)
        post_parser.add_argument('writer_url',type=str,required=True)
        post_parser.add_argument('novel',type=str,required=True)
        post_parser.add_argument('novel_url',type=str,required=True)
        post_parser.add_argument('country',type=str,required=True)
        post_parser.add_argument('order',type=int,required=True)
        return post_parser


    @staticmethod
    def export_update_parser():
        """
        define parser for update request 
        the order of novel is the only column allow for update 
        it don't make sence that we change novel name or writter 
        or even the contry of novel 
        """
        update_parser= reqparse.RequestParser()
        update_parser.add_argument('order',type=int,required=True)
        return update_parser


class NovelHelper():
    """
    heper class supports novel APIs
    """
    @staticmethod
    def abort_if_novel_not_exists(novel):
            """"
            ensure novel index already exists
            """
           
            excel_data = XLSXData.read_xlsx_novels_data()
            if novel not in \
            excel_data.loc[excel_data['الروايه']==novel]['الروايه'].to_list():
                abort(404, message="Novel {} Doesn't Exist".format(novel))
    
    @staticmethod
    def get_novel_obj(novel):
        """
        get novel object if exists by novel name
        """
        excel_data = XLSXData.read_xlsx_novels_data()
        return excel_data.loc[excel_data['الروايه']==novel]
    
