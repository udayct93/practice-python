# a='sample'
# b=10
# try:
#     if a=='' and b==10:
#         print('success')
#     else:
#         print('no')
#         raise Exception
# except Exception as e:
#    print("CMReconProcess: Error in Lambda: {}".format
# import AwsSESClient
from aws_ses_clientt import AwsSESClient

from cm_util import Constants, TicketProcessingStatus

eventss = {
    "Recordss": [
        {
            "awsRegion": "us-west-2",
            "dynamodb": {
                "ApproximateCreationDateTime": 1554359397,
                "Keys": {
                    "ConsolidatedMovementTransactionID": {
                        "S": "156412885048212"
                    }
                },
                "NewImage": {
                    "APIGravity": {
                        "NULL": True
                    },
                    "BOLDateTime": {
                        "S": "2019-08-01 09:26:00"
                    },
                    "BillOfLadingNumber": {
                        "S": "5109"
                    },
                    "BillOfLadingSource": {
                        "S": "TABS Data From DTN"
                    },
                    "CarrierFEIN": {
                        "NULL": True
                    },
                    "CarrierName": {
                        "S": "PILO"
                    },
                    "CarrierSCAC": {
                        "S": "PILO"
                    },
                    "ConsolidatedMovementTransactionID": {
                        "S": "1566960684961433"
                    },
                    "CustomerNumber": {
                        "NULL": True
                    },
                    "DestinationAddress": {
                        "NULL": True
                    },
                    "DestinationCity": {
                        "NULL": True
                    },
                    "DestinationCode": {
                        "NULL": True
                    },
                    "DestinationCustomerName": {
                        "NULL": True
                    },
                    "DestinationCustomerNumber": {
                        "S": "77703"
                    },
                    "DestinationState": {
                        "NULL": True
                    },
                    "DriverNumber": {
                        "NULL": True
                    },
                    "EndLoadDateTime": {
                        "S": "2019-08-01 09:26:00"
                    },
                    "FileName": {
                        "S": "dailymessages-2019-08-01-1030.csv-2019-08-01--10-30-15-335.csv"
                    },
                    "FilePath": {
                        "S": "pfj-cm-inbound-raw-dev/bol/csv/"
                    },
                    "GateInDateTime": {
                        "NULL": True
                    },
                    "Gravity": {
                        "NULL": True
                    },
                    "GrossGallons": {
                        "S": "4050.0"
                    },
                    "InvoiceNumber": {
                        "NULL": True
                    },
                    "NetGallons": {
                        "S": "4008.0"
                    },
                    "ProductCode": {
                        "S": "32"
                    },
                    "ProductDescription": {
                        "S": "ULS #2"
                    },
                    "PurchaseOrderNumber": {
                        "NULL": True
                    },
                    "Reason": {
                        "NULL": True
                    },
                    "ReleaseNumber": {
                        "NULL": True
                    },
                    "SPLCCode": {
                        "S": "434300"
                    },
                    "SpecificGravity": {
                        "NULL": True
                    },
                    "StartLoadDateTime": {
                        "S": "2019-08-01 09:18:00"
                    },
                    "Supplier": {
                        "S": "PILOT TRAVEL CENTERS"
                    },
                    "SupplierDefinedProduct": {
                        "S": "G2"
                    },
                    "SupplierDefinedTerminal": {
                        "NULL": True
                    },
                    "TCN": {
                        "S": "T62TN2204"
                    },
                    "TDTNBrandIndicator": {
                        "NULL": True
                    },
                    "TDTNOwnerName": {
                        "S": "TN Nashville Delek"
                    },
                    "Temperature": {
                        "NULL": True
                    },
                    "TerminalName": {
                        "S": "1979"
                    },
                    "TicketStatus": {
                        "S": "M"
                    },
                    "TransmissionDateTime": {
                        "S": "2019-08-01 09:28:00"
                    },
                    "TransmissionID": {
                        "N": "510908012019"
                    },
                    "Type": {
                        "NULL": True
                    },
                    "UnitOfMeasure": {
                        "S": "G"
                    },
                    "VehicleNumber": {
                        "S": "032240"
                    },
                    "VehicleType": {
                        "NULL": True
                    }
                },
                "SizeBytes": 1267
            },
            "eventName": "sa",
            "eventSource": "aws:dynamodb"
        }
    ]
}


def dummy_process(eventss, context):
    """This is the Lambda Handler function

    :param event: parameter to pass event data to handler
    :param context: parameter of type LambdaContext to get runtime information

    """
    billofladingnumber = get_bol_number(eventss)
    try:
        for message in eventss["Records"]:
            if message["eventName"] == "INSERT":
                new_record = message["dynamodb"]["NewImage"]

                ticket_status = new_record["TicketStatus"]["S"]
                if ticket_status == TicketProcessingStatus.READY.value:
                    try:
                        if new_record["BillOfLadingDateTime"] and new_record["BillOfLadingDateTime"]["S"]:
                            bol_parser = 'BOLParserFactory'.get_bol_parser(
                                new_record["BillOfLadingSource"]["S"])
                            if bol_parser:
                                bol_parser.process_bol(new_record)
                            else:
                                subject = Constants.CM_ERROR_SUBJECT.value.format(billofladingnumber)
                                body = Constants.CM_EMAIL_INVALID_BILLOFLADINGSOURCE_ERROR.value.format(
                                    billofladingnumber, new_record["BillOfLadingSource"]["S"])
                                AwsSESClient().send_email(subject, body)
                        else:
                            subject = Constants.CM_ERROR_SUBJECT.value.format(billofladingnumber)
                            body = Constants.CM_EMAIL_BILLOFLADINGDATETIME_NOT_FOUND.value.format(
                                billofladingnumber)
                            AwsSESClient().send_email(subject, body)

                    except KeyError as e:
                        subject = Constants.CM_ERROR_SUBJECT.value.format(new_record["BillOfLadingNumber"]["S"])
                        body = Constants.CM_EMAIL_BILLOFLADINGDATETIME_KEY_NOT_FOUND.value.format(
                            billofladingnumber, e)
                        AwsSESClient().send_email(subject, body)
                else:
                    subject = Constants.CM_ERROR_SUBJECT.value.format(new_record["BillOfLadingNumber"]["S"])
                    body = Constants.CM_EMAIL_IGNORING_TICKET_STATUS.value.format(new_record["BillOfLadingNumber"]["S"],
                                                                                  ticket_status,
                                                                                  TicketProcessingStatus.READY.value)
                    AwsSESClient().send_email(subject, body)
            else:
                subject = Constants.CM_ERROR_SUBJECT.value.format(billofladingnumber)
                body = Constants.CM_EMAIL_IGNORING_EVENT_NAME.value.format(billofladingnumber,
                                                                           message["eventName"])
                AwsSESClient().send_email(subject, body)
    except Exception as e:
        subject = Constants.CM_ERROR_SUBJECT.value.format(billofladingnumber)
        body = Constants.CM_EMAIL_EXCEPTION_ERROR.value.format(billofladingnumber, e)
        AwsSESClient().send_email(subject, body)


def get_bol_number(eventss):
    for message in eventss["Recordss"]:
        new_record = message["dynamodb"]["NewImage"]
        bol_no = new_record["BillOfLadingNumber"]["S"]
        return bol_no


dummy_process(eventss, None)
