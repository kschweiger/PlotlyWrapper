import logging
import os

def saveFigure(fig, height, width, staicFormat, filename, folder):
    """
    Args:
      height (int) : Image height
      width (int) : Image width
      staicFormat (str) : Choose from: png, jpeg, pdf, svg 
      filename (str) : File name
      folder (str) : Output folder
    
    Returns:
      True if finished or False if there is some error
    """
    if filename is None:
        logging.error("Please pass a filename. No plot will be saved")
        return False
    supportedFormats = ["png", "jpeg", "pdf", "svg"]
    if staicFormat not in supportedFormats:
        logging.error("Unsupported format passed: %s. Choose from %s", staicFormat, supportedFormats)
        logging.error("No plot will be saved")
        return False
    if not os.path.exists(folder):
        logging.warning("Creating folders: %s", folder)
        os.makedirs(folder)

    fig.update_layout(
        width=width, height=height
    )

    outputFile = folder+"/"+filename+"."+staicFormat
    logging.info("Writing output file: %s", outputFile)
    fig.write_image(outputFile)

    return True
