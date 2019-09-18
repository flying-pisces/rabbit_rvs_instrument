Partial Public Class MPK_API
    Function GetLastMeshData() As List(Of Single(,))
        Return ttAPI.GetMeasurementData()
    End Function

    Function GetRawData(imageKey As String) As List(Of Single(,))
        Return ttAPI.GetMeasurementData(imageKey)
    End Function
End Class
