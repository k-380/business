Attribute VB_Name = "BOMCompare"
Option Explicit

'===============================================================================
' Teamcenter BOM 差分比較マクロ
'
' 機能:
'   1. 旧BOM / 新BOM の Excel ファイルを選択
'   2. Teamcenter Excel RoundTrip の Custom XML から BOM を読み込む
'   3. レベル + リビジョン名をキーに LCS（最長共通部分列）で対応付け
'   4. 追加 / 削除 / 置換 / 数量変更を「差分」シートへ出力
'
' 特徴:
'   ・Excel上の列位置には依存しない
'   ・Teamcenter内部の propertyrealName を使って項目を特定する
'   ・比較対象ファイルは読み取り専用で開く
'
' Teamcenter内部プロパティ:
'   レベル       : bl_level_starting_0
'   数量         : bl_quantity
'   リビジョン名 : bl_rev_object_name
'===============================================================================


'===============================================================================
' メイン
'===============================================================================
Public Sub BOM比較()

    Dim oldFile As String
    Dim newFile As String

    Dim oldData As Collection
    Dim newData As Collection

    Dim ws As Worksheet

    On Error GoTo ErrorHandler

    Application.ScreenUpdating = False
    Application.DisplayAlerts = False


    '---------------------------------------------------------------------------
    ' 旧BOM選択
    '---------------------------------------------------------------------------
    oldFile = SelectExcelFile("旧BOMを選択してください")

    If oldFile = "" Then GoTo ExitHandler


    '---------------------------------------------------------------------------
    ' 新BOM選択
    '---------------------------------------------------------------------------
    newFile = SelectExcelFile("新BOMを選択してください")

    If newFile = "" Then GoTo ExitHandler


    '---------------------------------------------------------------------------
    ' BOM読み込み
    '---------------------------------------------------------------------------
    Set oldData = ReadTeamcenterBOM(oldFile)
    Set newData = ReadTeamcenterBOM(newFile)


    '---------------------------------------------------------------------------
    ' 差分シート準備
    '---------------------------------------------------------------------------
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets("差分")
    On Error GoTo ErrorHandler

    If ws Is Nothing Then

        Set ws = ThisWorkbook.Worksheets.Add( _
            After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))

        ws.Name = "差分"

    Else

        ws.Cells.Clear

    End If


    '---------------------------------------------------------------------------
    ' ヘッダー
    '---------------------------------------------------------------------------
    ws.Range("A1:H1").Value = Array( _
        "区分", _
        "旧レベル", _
        "旧リビジョン名", _
        "旧数量", _
        "新レベル", _
        "新リビジョン名", _
        "新数量", _
        "数量差")


    '---------------------------------------------------------------------------
    ' 比較
    '---------------------------------------------------------------------------
    CompareBOM oldData, newData, ws


    '---------------------------------------------------------------------------
    ' 見た目調整
    '---------------------------------------------------------------------------
    With ws

        .Rows(1).Font.Bold = True
        .Columns("A:H").AutoFit
        .Range("A1:H1").AutoFilter

        .Activate

    End With


    MsgBox _
        "BOM比較が完了しました。" & vbCrLf & vbCrLf & _
        "旧BOM：" & Dir(oldFile) & vbCrLf & _
        "新BOM：" & Dir(newFile), _
        vbInformation


ExitHandler:

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True

    Exit Sub


ErrorHandler:

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True

    MsgBox _
        "エラーが発生しました。" & vbCrLf & vbCrLf & _
        Err.Description, _
        vbCritical

End Sub


'===============================================================================
' Excelファイル選択
'===============================================================================
Private Function SelectExcelFile(titleText As String) As String

    Dim fd As FileDialog

    Set fd = Application.FileDialog(msoFileDialogFilePicker)

    With fd

        .Title = titleText
        .AllowMultiSelect = False

        .Filters.Clear
        .Filters.Add "Excelファイル", "*.xlsm;*.xlsx"

        If .Show = -1 Then

            SelectExcelFile = .SelectedItems(1)

        Else

            SelectExcelFile = ""

        End If

    End With

End Function


'===============================================================================
' Teamcenter BOM読み込み
'
' 列記号(A、B、C...)には依存せず、
' Teamcenter内部の propertyrealName で項目を判定する。
'
' 戻り値:
'   Collection
'
' 各要素:
'   Array(Level, RevisionName, Quantity)
'===============================================================================
Private Function ReadTeamcenterBOM(filePath As String) As Collection

    Const PROP_LEVEL As String = "bl_level_starting_0"
    Const PROP_QUANTITY As String = "bl_quantity"
    Const PROP_REVISION_NAME As String = "bl_rev_object_name"

    Dim wb As Workbook

    Dim result As New Collection

    Dim xmlPart As Object
    Dim xmlDoc As Object

    Dim objectNodes As Object
    Dim objectNode As Object

    Dim propNodes As Object
    Dim propNode As Object

    Dim propertyRealName As String

    Dim levelText As String
    Dim quantityText As String
    Dim revisionName As String

    Dim levelValue As Variant
    Dim quantityValue As Variant

    Dim foundXML As Boolean
    Dim foundLevelProperty As Boolean
    Dim foundQuantityProperty As Boolean
    Dim foundRevisionProperty As Boolean

    Dim savedErrNumber As Long
    Dim savedErrDescription As String

    On Error GoTo ErrorHandler


    '---------------------------------------------------------------------------
    ' BOMファイルを読み取り専用で開く
    '---------------------------------------------------------------------------
    Set wb = Workbooks.Open( _
        Filename:=filePath, _
        ReadOnly:=True, _
        UpdateLinks:=False)


    '---------------------------------------------------------------------------
    ' Custom XMLを順番に調べる
    '---------------------------------------------------------------------------
    For Each xmlPart In wb.CustomXMLParts

        Set xmlDoc = CreateObject("MSXML2.DOMDocument.6.0")

        xmlDoc.async = False

        If xmlDoc.LoadXML(xmlPart.XML) Then

            Set objectNodes = xmlDoc.SelectNodes( _
                "//*[local-name()='ObjectData']")

            If objectNodes.Length > 0 Then

                foundXML = True

                '----------------------------------------------------------------
                ' BOMを1行ずつ読む
                '----------------------------------------------------------------
                For Each objectNode In objectNodes

                    levelText = ""
                    quantityText = ""
                    revisionName = ""

                    Set propNodes = objectNode.SelectNodes( _
                        "*[local-name()='PropertyData']")

                    For Each propNode In propNodes

                        propertyRealName = LCase$(Trim$( _
                            GetAttributeText(propNode, "propertyrealName")))

                        '念のため表記揺れにも対応
                        If propertyRealName = "" Then
                            propertyRealName = LCase$(Trim$( _
                                GetAttributeText(propNode, "propertyRealName")))
                        End If

                        Select Case propertyRealName

                            Case LCase$(PROP_LEVEL)

                                levelText = GetAttributeText(propNode, "value")
                                foundLevelProperty = True

                            Case LCase$(PROP_QUANTITY)

                                quantityText = GetAttributeText(propNode, "value")
                                foundQuantityProperty = True

                            Case LCase$(PROP_REVISION_NAME)

                                revisionName = GetAttributeText(propNode, "value")
                                foundRevisionProperty = True

                        End Select

                    Next propNode


                    '----------------------------------------------------------------
                    ' リビジョン名が空欄の行は無視
                    '----------------------------------------------------------------
                    If revisionName <> "" Then

                        If IsNumeric(levelText) Then

                            levelValue = CLng(levelText)

                        Else

                            levelValue = Empty

                        End If


                        If IsNumeric(quantityText) Then

                            quantityValue = CDbl(quantityText)

                        Else

                            quantityValue = Empty

                        End If


                        result.Add Array( _
                            levelValue, _
                            revisionName, _
                            quantityValue)

                    End If

                Next objectNode

                Exit For

            End If

        End If

    Next xmlPart


    wb.Close SaveChanges:=False
    Set wb = Nothing


    '---------------------------------------------------------------------------
    ' 必要データの存在チェック
    '---------------------------------------------------------------------------
    If foundXML = False Then

        Err.Raise _
            vbObjectError + 1000, _
            "ReadTeamcenterBOM", _
            "Teamcenter BOMのXMLデータが見つかりませんでした。"

    End If


    If foundLevelProperty = False Then

        Err.Raise _
            vbObjectError + 1001, _
            "ReadTeamcenterBOM", _
            "レベル情報（bl_level_starting_0）が見つかりませんでした。"

    End If


    If foundQuantityProperty = False Then

        Err.Raise _
            vbObjectError + 1002, _
            "ReadTeamcenterBOM", _
            "数量情報（bl_quantity）が見つかりませんでした。"

    End If


    If foundRevisionProperty = False Then

        Err.Raise _
            vbObjectError + 1003, _
            "ReadTeamcenterBOM", _
            "リビジョン名（bl_rev_object_name）が見つかりませんでした。"

    End If


    Set ReadTeamcenterBOM = result

    Exit Function


ErrorHandler:

    savedErrNumber = Err.Number
    savedErrDescription = Err.Description

    On Error Resume Next

    If Not wb Is Nothing Then
        wb.Close SaveChanges:=False
    End If

    On Error GoTo 0

    Err.Raise _
        savedErrNumber, _
        "ReadTeamcenterBOM", _
        savedErrDescription

End Function


'===============================================================================
' XML属性を文字列で安全に取得
'===============================================================================
Private Function GetAttributeText(node As Object, attributeName As String) As String

    Dim v As Variant

    On Error Resume Next
    v = node.getAttribute(attributeName)
    On Error GoTo 0

    If IsNull(v) Or IsEmpty(v) Then

        GetAttributeText = ""

    Else

        GetAttributeText = CStr(v)

    End If

End Function


'===============================================================================
' BOM比較
'
' LCS（Longest Common Subsequence: 最長共通部分列）を使って、
' レベル + リビジョン名が一致する行を、並び順を保ちながら対応付ける。
'
' 数量はLCSキーに含めない。
' 同じ部品の数量だけが変わった場合は「数量変更」として検出する。
'
' 「置換」は以下の条件による推定:
'   ・現在位置の旧/新レベルが同じ
'   ・旧行と新行を1行ずつ進めても、その後の最大LCS長が維持される
'===============================================================================
Private Sub CompareBOM( _
    oldData As Collection, _
    newData As Collection, _
    ws As Worksheet)

    Dim n As Long
    Dim m As Long

    Dim dp() As Long

    Dim i As Long
    Dim j As Long

    Dim outputRow As Long

    Dim oldRow As Variant
    Dim newRow As Variant


    n = oldData.Count
    m = newData.Count


    '---------------------------------------------------------------------------
    ' dp(i,j) = old(i..n) と new(j..m) のLCS長
    ' n+1 / m+1 は末尾の番兵領域
    '---------------------------------------------------------------------------
    ReDim dp(1 To n + 1, 1 To m + 1)


    '---------------------------------------------------------------------------
    ' LCSテーブル作成
    '---------------------------------------------------------------------------
    For i = n To 1 Step -1

        For j = m To 1 Step -1

            If BOMKey(oldData(i)) = BOMKey(newData(j)) Then

                dp(i, j) = dp(i + 1, j + 1) + 1

            ElseIf dp(i + 1, j) >= dp(i, j + 1) Then

                dp(i, j) = dp(i + 1, j)

            Else

                dp(i, j) = dp(i, j + 1)

            End If

        Next j

    Next i


    '---------------------------------------------------------------------------
    ' 差分復元
    '---------------------------------------------------------------------------
    i = 1
    j = 1
    outputRow = 2


    Do While i <= n Or j <= m


        '-----------------------------------------------------------------------
        ' 両方に行が残っている
        '-----------------------------------------------------------------------
        If i <= n And j <= m Then

            oldRow = oldData(i)
            newRow = newData(j)


            '-------------------------------------------------------------------
            ' 同じレベル・同じリビジョン名
            '-------------------------------------------------------------------
            If BOMKey(oldRow) = BOMKey(newRow) Then

                If Not QuantityEqual(oldRow(2), newRow(2)) Then

                    WriteDiffRow _
                        ws, _
                        outputRow, _
                        "数量変更", _
                        oldRow, _
                        newRow

                    outputRow = outputRow + 1

                End If

                i = i + 1
                j = j + 1


            '-------------------------------------------------------------------
            ' 同じレベルで、双方を1行進めても今後のLCSを失わない場合
            ' → 置換と推定
            '-------------------------------------------------------------------
            ElseIf SameLevel(oldRow, newRow) _
                And dp(i + 1, j + 1) = dp(i, j) Then

                WriteDiffRow _
                    ws, _
                    outputRow, _
                    "置換", _
                    oldRow, _
                    newRow

                outputRow = outputRow + 1

                i = i + 1
                j = j + 1


            '-------------------------------------------------------------------
            ' 新側を1行進めた方がLCSが維持される
            ' → 新側の行は追加
            '-------------------------------------------------------------------
            ElseIf dp(i, j + 1) >= dp(i + 1, j) Then

                WriteDiffRow _
                    ws, _
                    outputRow, _
                    "追加", _
                    Empty, _
                    newRow

                outputRow = outputRow + 1

                j = j + 1


            '-------------------------------------------------------------------
            ' 旧側の行は削除
            '-------------------------------------------------------------------
            Else

                WriteDiffRow _
                    ws, _
                    outputRow, _
                    "削除", _
                    oldRow, _
                    Empty

                outputRow = outputRow + 1

                i = i + 1

            End If


        '-----------------------------------------------------------------------
        ' 旧側だけ残った
        '-----------------------------------------------------------------------
        ElseIf i <= n Then

            oldRow = oldData(i)

            WriteDiffRow _
                ws, _
                outputRow, _
                "削除", _
                oldRow, _
                Empty

            outputRow = outputRow + 1
            i = i + 1


        '-----------------------------------------------------------------------
        ' 新側だけ残った
        '-----------------------------------------------------------------------
        ElseIf j <= m Then

            newRow = newData(j)

            WriteDiffRow _
                ws, _
                outputRow, _
                "追加", _
                Empty, _
                newRow

            outputRow = outputRow + 1
            j = j + 1

        End If

    Loop

End Sub


'===============================================================================
' BOM比較キー
'===============================================================================
Private Function BOMKey(rowData As Variant) As String

    BOMKey = _
        VariantToText(rowData(0)) & "|" & _
        CStr(rowData(1))

End Function


'===============================================================================
' 同一レベル判定
'===============================================================================
Private Function SameLevel(oldRow As Variant, newRow As Variant) As Boolean

    If IsEmpty(oldRow(0)) Or IsEmpty(newRow(0)) Then

        SameLevel = False

    Else

        SameLevel = (CLng(oldRow(0)) = CLng(newRow(0)))

    End If

End Function


'===============================================================================
' Variantを比較キー用文字列へ変換
'===============================================================================
Private Function VariantToText(v As Variant) As String

    If IsEmpty(v) Or IsNull(v) Then

        VariantToText = ""

    Else

        VariantToText = CStr(v)

    End If

End Function


'===============================================================================
' 数量比較
'===============================================================================
Private Function QuantityEqual(a As Variant, b As Variant) As Boolean

    Const TOLERANCE As Double = 0.000000001

    If IsEmpty(a) And IsEmpty(b) Then

        QuantityEqual = True
        Exit Function

    End If


    If IsEmpty(a) Or IsEmpty(b) Then

        QuantityEqual = False
        Exit Function

    End If


    QuantityEqual = _
        Abs(CDbl(a) - CDbl(b)) <= TOLERANCE

End Function


'===============================================================================
' 差分行出力
'===============================================================================
Private Sub WriteDiffRow( _
    ws As Worksheet, _
    rowNo As Long, _
    diffType As String, _
    oldRow As Variant, _
    newRow As Variant)

    ws.Cells(rowNo, 1).Value = diffType


    '---------------------------------------------------------------------------
    ' 旧BOM
    '---------------------------------------------------------------------------
    If IsArray(oldRow) Then

        If Not IsEmpty(oldRow(0)) Then
            ws.Cells(rowNo, 2).Value = oldRow(0)
        End If

        ws.Cells(rowNo, 3).Value = oldRow(1)

        If Not IsEmpty(oldRow(2)) Then
            ws.Cells(rowNo, 4).Value = oldRow(2)
        End If

    End If


    '---------------------------------------------------------------------------
    ' 新BOM
    '---------------------------------------------------------------------------
    If IsArray(newRow) Then

        If Not IsEmpty(newRow(0)) Then
            ws.Cells(rowNo, 5).Value = newRow(0)
        End If

        ws.Cells(rowNo, 6).Value = newRow(1)

        If Not IsEmpty(newRow(2)) Then
            ws.Cells(rowNo, 7).Value = newRow(2)
        End If

    End If


    '---------------------------------------------------------------------------
    ' 数量差 = 新数量 - 旧数量
    '---------------------------------------------------------------------------
    If IsArray(oldRow) And IsArray(newRow) Then

        If Not IsEmpty(oldRow(2)) _
            And Not IsEmpty(newRow(2)) Then

            ws.Cells(rowNo, 8).Value = _
                CDbl(newRow(2)) - CDbl(oldRow(2))

        End If

    End If

End Sub
