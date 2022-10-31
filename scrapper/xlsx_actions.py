import pandas as pd 
from flask_restful import abort

class XLSXData(object):
    """
    handle read excel as dataframe 
    handle export data frame as excel
    """


    sheet_name: str = "Novels"
    workbook_name: str = "WikiScrapping.xlsx"
    headers: list[str] = ['الروايه', 'عنوان الروايه', 'الكاتب', 'عنوان الكاتب', 'البلد', 'الترتيب']
    @staticmethod 
    def read_xlsx_novels_data():
        """
        read/reread xlsx data as pandas data frame
        """
        try:
                xlsx_data =pd.read_excel(XLSXData.workbook_name,XLSXData.sheet_name)
                if list(xlsx_data.columns) != XLSXData.headers:
                    abort(400,message=f"xlsx sheet headers don't match {XLSXData.headers} raw headers f{list(xlsx_data.columns)}")
                return xlsx_data
        except ValueError:
               abort(400,message=f"sheet {XLSXData.sheet_name} not found in excel workbook {XLSXData.workbook_name}")
        except FileNotFoundError:
               abort(400,message=f"make sure data scrapping export in {XLSXData.workbook_name} on sheet {XLSXData.sheet_name}")


    @staticmethod
    def export_edited_novels_data(data_frame):
        """
        write/rewrite data pandas data frame to excel sheets
        rewrite excel sheet after add new one or edit existing one or delete one
        """
        try:
                df = pd.DataFrame(data_frame)
                df.to_excel(XLSXData.workbook_name,XLSXData.sheet_name,index=False,header=True,index_label="Index")
        except Exception as E:
                return {
                    "message":f"thanks to ensure that requirements libraries already installerd and workbook {XLSXData.workbook_name} closed"
                } , 400
