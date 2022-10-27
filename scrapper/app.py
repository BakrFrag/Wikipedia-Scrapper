from flask import Flask , request
from flask_restful import  Api, Resource
import pandas as pd
from helpers import NovelParser , NovelHelper
from xlsx_actions import  XLSXData
app = Flask(__name__)
api = Api(app)


class NovelsAPIS(Resource):
    def get(self):
       """
       convert excel data frame to list of dict that can rendered as json  
       """
       excel_data = XLSXData.read_xlsx_novels_data()
       return excel_data.to_dict('records')

    def post(self):
        """
        create novel object if novel not exists 
        """
        post_parser = NovelParser.export_post_parser()
        parser = post_parser.parse_args()
        row= {
            "الروايه":parser['novel'].strip(),
            "عنوان الروايه":parser['novel_url'].strip(),
            "الكاتب":parser['writer'].strip(),
            "عنوان الكاتب":parser['writer_url'].strip(),
            "البلد":parser['country'].strip(),
            "الترتيب":parser['order']
        }
        excel_data = XLSXData.read_xlsx_novels_data()
        
        if parser['novel'] not in excel_data.loc[excel_data['الروايه']==parser['novel']]['الروايه'].to_list():
           
                row= pd.DataFrame([row])
                data = pd.concat([excel_data,row],ignore_index=True)
                XLSXData.export_edited_novels_data(data)
                return {
                    "novel":parser['novel']
                } , 201
        return {
                "mesaage": f"novel {parser['novel']} already exists"
            } , 400


class NovelObjectAPI(Resource):

    def get(self,novel):
        """
        get single object by novel name
        """
        novel=novel.strip()
        NovelHelper.abort_if_novel_not_exists(novel)
        novel_obj = NovelHelper.get_novel_obj(novel)
        return  novel_obj.to_dict('records') , 200
        


    def put(self,novel):
        """
        update novel order by novel name
        the only editable field is order of novel 
        it don't make sense that novel name today with name and 
        """
        
        novel=novel.strip()
        NovelHelper.abort_if_novel_not_exists(novel)
        update_parser = NovelParser.export_update_parser()
        parser=update_parser.parse_args()
        order=parser['order']
        novel_obj=NovelHelper.get_novel_obj(novel)
        excel_data=XLSXData.read_xlsx_novels_data()
        excel_data.loc[novel_obj.index, ['الترتيب']]=order
        XLSXData.export_edited_novels_data(excel_data)
        return  {
            "novel":f"novel {novel} order updated with new oder {order}"
        }
        

        
    def delete(self,novel):
        """
        delete novel by novel name 
        """
        novel=novel.strip()
        NovelHelper.abort_if_novel_not_exists(novel)
        novel_obj=NovelHelper.get_novel_obj(novel)
        excel_data=XLSXData.read_xlsx_novels_data()
        excel_data=excel_data.drop(novel_obj.index,axis=0)
        XLSXData.export_edited_novels_data(excel_data)
        return  {
            
        } , 204
    

api.add_resource(NovelsAPIS,"/")
api.add_resource(NovelObjectAPI,"/<string:novel>")
if __name__=='__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)