
class FileIO:

    def read(self,filename,offset,length):
        """ Read data from a file.
        @param filename The file to read from.
        @param offset   The offset to start reading from.
        @param length   The number of bytes to read.
        @return The data read or '' in case of error.
        """
        pass
        
    def write(self,filename,offset,block):
        """ Write data to a file.
        @param filename The file to write to.
        @param offset   The offset to write at.
        @param block    The block of data to write.
        @return The number of bytes written or -1 in case of error.
        """
        pass
