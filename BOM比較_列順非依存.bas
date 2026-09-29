Attribute VB_Name = "BOMCompare"
Option Explicit

'===============================================================================
' Teamcenter BOM 差分比較マクロ
'
' 【機能】
'   1. 旧BOM / 新BOM の Excel ファイルを選択
'   2. Teamcenter Excel RoundTrip の Custom XML から BOM を読み込む
'   3. レベル + リビジョン名をキーとしてLCSで対応付け
'   4. 数量変更 / 置換 / 追加 / 削除を抽出
'   5. 「差分」シートへ結果を一覧表示
'   6. 新BOMと同じフォルダへ比較結果.xlsxを自動出力
'
' 【列順非依存】
'   Excel上の列位置には依存しない。
'   Teamcenter内部の propertyrealName を使って項目を特定する。
'
'   レベル       = bl_level_starting_0
'   数量         = bl_quantity
'   リビジョン名 = bl_rev_object_name
'
' 【比較方法】
'   LCS（最長共通部分列）で確実に一致する行をアンカーとして確定し、
'   アンカー間に残った未一致ブロックを後から判定する。
'
'   未一致ブロックが同じ行数かつ各位置のレベルが一致する場合だけ
'   「置換」とみなす。
'   対応が曖昧な大きなブロックは無理に置換せず、
'   「削除」と「追加」に分けて表示する。
'
' 【自動出力】
'   旧: MF2299.xlsm
'   新: MF2300.xlsm
'
'   → BOM比較_MF2299_to_MF2300.xlsx
'
'   同名ファイルが存在する場合は日時を付加する。
'===============================================================================


'===============================================================================
' メイン処理
'===============================================================================
Public Sub BOM比較()

    Dim oldFile As String
    Dim newFile As String
    Dim outputFile As String

    Dim oldData As Collection
    Dim newData As Collection
    Dim diffData As Collection

    Dim ws As Worksheet

    Dim oldCount As Long
    Dim newCount As Long

    On Error GoTo ErrorHandler

    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    Application.EnableEvents = False


    '===========================================================================
    ' 旧BOM選択
    '===========================================================================
    oldFile = SelectExcelFile( _
        "旧BOM（変更前）を選択してください")

    If oldFile = "" Then
        GoTo ExitHandler
    End If


    '===========================================================================
    ' 新BOM選択
    '===========================================================================
    newFile = SelectExcelFile( _
        "新BOM（変更後）を選択してください")

    If newFile = "" Then
        GoTo ExitHandler
    End If


    '===========================================================================
    ' 同じファイルを選んでいないか確認
    '===========================================================================
    If StrComp( _
        oldFile, _
        newFile, _
        vbTextCompare) = 0 Then

        MsgBox _
            "旧BOMと新BOMに同じファイルが選択されています。", _
            vbExclamation

        GoTo ExitHandler

    End If


    '===========================================================================
    ' BOM読み込み
    '===========================================================================
    Set oldData = ReadTeamcenterBOM(oldFile)
    Set newData = ReadTeamcenterBOM(newFile)

    oldCount = oldData.Count
    newCount = newData.Count


    '===========================================================================
    ' BOM比較
    '===========================================================================
    Set diffData = CompareBOM( _
        oldData, _
        newData)


    '===========================================================================
    ' 差分シート準備
    '===========================================================================
    Set ws = PrepareResultSheet()


    '===========================================================================
    ' 結果表示
    '===========================================================================
    WriteResults _
        ws, _
        diffData


    '===========================================================================
    ' 書式設定
    '===========================================================================
    FormatResultSheet ws


    '===========================================================================
    ' 比較結果を別Excelファイルとして自動保存
    '===========================================================================
    outputFile = ExportComparisonResult( _
        ws, _
        oldFile, _
        newFile)


    '===========================================================================
    ' 完了表示
    '===========================================================================
    MsgBox _
        "BOM比較が完了しました。" & vbCrLf & _
        vbCrLf & _
        "旧BOM：" & Dir(oldFile) & vbCrLf & _
        "行数：" & oldCount & vbCrLf & _
        vbCrLf & _
        "新BOM：" & Dir(newFile) & vbCrLf & _
        "行数：" & newCount & vbCrLf & _
        vbCrLf & _
        "差分：" & diffData.Count & " 件" & vbCrLf & _
        vbCrLf & _
        "比較結果を保存しました。" & vbCrLf & _
        outputFile, _
        vbInformation


ExitHandler:

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    Application.EnableEvents = True

    Exit Sub


ErrorHandler:

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    Application.EnableEvents = True

    MsgBox _
        "エラーが発生しました。" & vbCrLf & _
        vbCrLf & _
        Err.Description, _
        vbCritical

End Sub


'===============================================================================
' ファイル選択
'===============================================================================
Private Function SelectExcelFile( _
    titleText As String) As String

    Dim fd As FileDialog

    Set fd = Application.FileDialog( _
        msoFileDialogFilePicker)

    With fd

        .Title = titleText
        .AllowMultiSelect = False

        .Filters.Clear
        .Filters.Add _
            "Excelファイル", _
            "*.xlsm;*.xlsx"

        If .Show = -1 Then

            SelectExcelFile = _
                .SelectedItems(1)

        Else

            SelectExcelFile = ""

        End If

    End With

End Function


'===============================================================================
' Teamcenter BOM読み込み
'
' 戻り値:
'   Collection
'
' 各行:
'   Array(
'       レベル,
'       リビジョン名,
'       数量
'   )
'===============================================================================
Private Function ReadTeamcenterBOM( _
    filePath As String) As Collection

    Const PROP_LEVEL As String = _
        "bl_level_starting_0"

    Const PROP_QUANTITY As String = _
        "bl_quantity"

    Const PROP_REVISION_NAME As String = _
        "bl_rev_object_name"

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


    '===========================================================================
    ' BOMを読み取り専用で開く
    '===========================================================================
    Set wb = Workbooks.Open( _
        Filename:=filePath, _
        ReadOnly:=True, _
        UpdateLinks:=False)


    '===========================================================================
    ' Custom XMLを探索
    '===========================================================================
    For Each xmlPart In wb.CustomXMLParts

        Set xmlDoc = CreateObject( _
            "MSXML2.DOMDocument.6.0")

        xmlDoc.async = False

        If xmlDoc.LoadXML( _
            xmlPart.XML) Then

            Set objectNodes = _
                xmlDoc.SelectNodes( _
                "//*[local-name()='ObjectData']")

            If objectNodes.Length > 0 Then

                foundXML = True

                '===============================================================
                ' BOM行を順番に読む
                '===============================================================
                For Each objectNode In objectNodes

                    levelText = ""
                    quantityText = ""
                    revisionName = ""

                    Set propNodes = _
                        objectNode.SelectNodes( _
                        "*[local-name()='PropertyData']")

                    '-----------------------------------------------------------
                    ' 各プロパティを読む
                    '-----------------------------------------------------------
                    For Each propNode In propNodes

                        propertyRealName = _
                            LCase$( _
                            Trim$( _
                            GetAttributeText( _
                                propNode, _
                                "propertyrealName")))

                        '-------------------------------------------------------
                        ' 大文字R表記にも念のため対応
                        '-------------------------------------------------------
                        If propertyRealName = "" Then

                            propertyRealName = _
                                LCase$( _
                                Trim$( _
                                GetAttributeText( _
                                    propNode, _
                                    "propertyRealName")))

                        End If

                        Select Case propertyRealName

                            Case LCase$(PROP_LEVEL)

                                levelText = _
                                    GetAttributeText( _
                                        propNode, _
                                        "value")

                                foundLevelProperty = True

                            Case LCase$(PROP_QUANTITY)

                                quantityText = _
                                    GetAttributeText( _
                                        propNode, _
                                        "value")

                                foundQuantityProperty = True

                            Case LCase$(PROP_REVISION_NAME)

                                revisionName = _
                                    GetAttributeText( _
                                        propNode, _
                                        "value")

                                foundRevisionProperty = True

                        End Select

                    Next propNode


                    '===========================================================
                    ' リビジョン名が存在する行のみ登録
                    '===========================================================
                    If revisionName <> "" Then

                        If IsNumeric(levelText) Then

                            levelValue = _
                                CLng(levelText)

                        Else

                            levelValue = Empty

                        End If

                        If IsNumeric(quantityText) Then

                            quantityValue = _
                                CDbl(quantityText)

                        Else

                            quantityValue = Empty

                        End If

                        result.Add _
                            Array( _
                                levelValue, _
                                revisionName, _
                                quantityValue)

                    End If

                Next objectNode

                Exit For

            End If

        End If

    Next xmlPart


    '===========================================================================
    ' BOMファイルを閉じる
    '===========================================================================
    wb.Close _
        SaveChanges:=False

    Set wb = Nothing


    '===========================================================================
    ' XMLチェック
    '===========================================================================
    If foundXML = False Then

        Err.Raise _
            vbObjectError + 1000, _
            "ReadTeamcenterBOM", _
            "Teamcenter BOMのXMLデータが見つかりませんでした。"

    End If


    '===========================================================================
    ' レベルチェック
    '===========================================================================
    If foundLevelProperty = False Then

        Err.Raise _
            vbObjectError + 1001, _
            "ReadTeamcenterBOM", _
            "レベル情報（bl_level_starting_0）が見つかりませんでした。"

    End If


    '===========================================================================
    ' 数量チェック
    '===========================================================================
    If foundQuantityProperty = False Then

        Err.Raise _
            vbObjectError + 1002, _
            "ReadTeamcenterBOM", _
            "数量情報（bl_quantity）が見つかりませんでした。"

    End If


    '===========================================================================
    ' リビジョン名チェック
    '===========================================================================
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

        wb.Close _
            SaveChanges:=False

    End If

    On Error GoTo 0

    Err.Raise _
        savedErrNumber, _
        "ReadTeamcenterBOM", _
        savedErrDescription

End Function


'===============================================================================
' XML属性を安全に取得
'===============================================================================
Private Function GetAttributeText( _
    node As Object, _
    attributeName As String) As String

    Dim v As Variant

    On Error Resume Next

    v = node.getAttribute( _
        attributeName)

    On Error GoTo 0

    If IsNull(v) _
        Or IsEmpty(v) Then

        GetAttributeText = ""

    Else

        GetAttributeText = CStr(v)

    End If

End Function


'===============================================================================
' BOM比較
'
' 戻り値:
'
' Collection
'
' 各要素:
'
' Array(
'   区分,
'   旧レベル,
'   旧リビジョン名,
'   旧数量,
'   新レベル,
'   新リビジョン名,
'   新数量,
'   数量差
' )
'
' 【処理の考え方】
'
' 1. LCSを計算
' 2. LCSで完全一致した行を「アンカー」として取得
' 3. アンカー間に残った行をブロック単位で比較
' 4. 旧/新の行数が同じで、各位置のレベルも同じ場合だけ「置換」
' 5. 対応が曖昧な大きなブロックは「削除」「追加」として表示
'===============================================================================
Private Function CompareBOM( _
    oldData As Collection, _
    newData As Collection) As Collection

    Dim result As New Collection

    Dim n As Long
    Dim m As Long

    Dim dp() As Long

    Dim i As Long
    Dim j As Long

    Dim matches As Collection
    Dim matchData As Variant

    Dim prevOld As Long
    Dim prevNew As Long

    Dim matchOld As Long
    Dim matchNew As Long

    Dim oldRow As Variant
    Dim newRow As Variant


    n = oldData.Count
    m = newData.Count


    '===========================================================================
    ' 空データ対策
    '===========================================================================
    If n = 0 _
        And m = 0 Then

        Set CompareBOM = result

        Exit Function

    End If


    '===========================================================================
    ' LCS DPテーブル
    '
    ' dp(i,j)
    '
    ' 旧BOM i行目以降
    ' 新BOM j行目以降
    '
    ' の最大共通部分列長
    '===========================================================================
    ReDim dp( _
        1 To n + 1, _
        1 To m + 1)


    '===========================================================================
    ' LCS計算
    '===========================================================================
    For i = n To 1 Step -1

        For j = m To 1 Step -1

            If BOMKey(oldData(i)) = _
               BOMKey(newData(j)) Then

                dp(i, j) = _
                    dp(i + 1, j + 1) + 1

            ElseIf _
                dp(i + 1, j) >= _
                dp(i, j + 1) Then

                dp(i, j) = _
                    dp(i + 1, j)

            Else

                dp(i, j) = _
                    dp(i, j + 1)

            End If

        Next j

    Next i


    '===========================================================================
    ' LCSアンカー取得
    '===========================================================================
    Set matches = New Collection

    i = 1
    j = 1

    Do While _
        i <= n _
        And j <= m

        If BOMKey(oldData(i)) = _
           BOMKey(newData(j)) Then

            matches.Add _
                Array(i, j)

            i = i + 1
            j = j + 1

        ElseIf _
            dp(i + 1, j) >= _
            dp(i, j + 1) Then

            i = i + 1

        Else

            j = j + 1

        End If

    Loop


    '===========================================================================
    ' 最後の番兵
    '
    ' BOM末尾の差分ブロックを処理するため、
    ' old = n + 1 / new = m + 1 を仮想アンカーとして追加
    '===========================================================================
    matches.Add _
        Array( _
            n + 1, _
            m + 1)

    prevOld = 0
    prevNew = 0


    '===========================================================================
    ' アンカー間を処理
    '===========================================================================
    For Each matchData In matches

        matchOld = CLng( _
            matchData(0))

        matchNew = CLng( _
            matchData(1))


        '=======================================================================
        ' アンカーの前にある未一致ブロック
        '=======================================================================
        ProcessUnmatchedBlock _
            oldData, _
            newData, _
            prevOld + 1, _
            matchOld - 1, _
            prevNew + 1, _
            matchNew - 1, _
            result


        '=======================================================================
        ' 本物のアンカーの場合
        '=======================================================================
        If matchOld <= n _
            And matchNew <= m Then

            oldRow = oldData(matchOld)
            newRow = newData(matchNew)

            '-------------------------------------------------------------------
            ' 同じ部品だが数量が違う
            '-------------------------------------------------------------------
            If Not QuantityEqual( _
                oldRow(2), _
                newRow(2)) Then

                AddDiff _
                    result, _
                    "数量変更", _
                    oldRow, _
                    newRow

            End If

        End If

        prevOld = matchOld
        prevNew = matchNew

    Next matchData


    Set CompareBOM = result

End Function


'===============================================================================
' LCSアンカー間の未一致ブロックを処理
'===============================================================================
Private Sub ProcessUnmatchedBlock( _
    oldData As Collection, _
    newData As Collection, _
    oldStart As Long, _
    oldEnd As Long, _
    newStart As Long, _
    newEnd As Long, _
    result As Collection)

    Dim oldCount As Long
    Dim newCount As Long

    Dim i As Long

    Dim oldRow As Variant
    Dim newRow As Variant

    Dim canReplace As Boolean


    '===========================================================================
    ' 行数計算
    '===========================================================================
    If oldStart <= oldEnd Then

        oldCount = _
            oldEnd - oldStart + 1

    Else

        oldCount = 0

    End If


    If newStart <= newEnd Then

        newCount = _
            newEnd - newStart + 1

    Else

        newCount = 0

    End If


    '===========================================================================
    ' 差分なし
    '===========================================================================
    If oldCount = 0 _
        And newCount = 0 Then

        Exit Sub

    End If


    '===========================================================================
    ' 新側だけ存在 → 追加
    '===========================================================================
    If oldCount = 0 Then

        For i = newStart To newEnd

            newRow = newData(i)

            AddDiff _
                result, _
                "追加", _
                Empty, _
                newRow

        Next i

        Exit Sub

    End If


    '===========================================================================
    ' 旧側だけ存在 → 削除
    '===========================================================================
    If newCount = 0 Then

        For i = oldStart To oldEnd

            oldRow = oldData(i)

            AddDiff _
                result, _
                "削除", _
                oldRow, _
                Empty

        Next i

        Exit Sub

    End If


    '===========================================================================
    ' 旧と新の行数が同じ場合
    '
    ' さらに各位置のレベルが一致する場合のみ
    ' 1対1の置換候補とみなす
    '===========================================================================
    canReplace = False

    If oldCount = newCount Then

        canReplace = True

        For i = 0 To oldCount - 1

            oldRow = _
                oldData(oldStart + i)

            newRow = _
                newData(newStart + i)

            If Not SameLevel( _
                oldRow, _
                newRow) Then

                canReplace = False

                Exit For

            End If

        Next i

    End If


    '===========================================================================
    ' 1対1対応可能
    '===========================================================================
    If canReplace Then

        For i = 0 To oldCount - 1

            oldRow = _
                oldData(oldStart + i)

            newRow = _
                newData(newStart + i)

            If BOMKey(oldRow) = _
               BOMKey(newRow) Then

                If Not QuantityEqual( _
                    oldRow(2), _
                    newRow(2)) Then

                    AddDiff _
                        result, _
                        "数量変更", _
                        oldRow, _
                        newRow

                End If

            Else

                AddDiff _
                    result, _
                    "置換", _
                    oldRow, _
                    newRow

            End If

        Next i

        Exit Sub

    End If


    '===========================================================================
    ' 対応が曖昧なブロック
    '
    ' 無理に置換として結びつけず、
    ' 旧側 → 削除
    ' 新側 → 追加
    ' として表示
    '===========================================================================
    For i = oldStart To oldEnd

        oldRow = oldData(i)

        AddDiff _
            result, _
            "削除", _
            oldRow, _
            Empty

    Next i


    For i = newStart To newEnd

        newRow = newData(i)

        AddDiff _
            result, _
            "追加", _
            Empty, _
            newRow

    Next i

End Sub


'===============================================================================
' 差分1件をCollectionへ追加
'===============================================================================
Private Sub AddDiff( _
    result As Collection, _
    diffType As String, _
    oldRow As Variant, _
    newRow As Variant)

    Dim oldLevel As Variant
    Dim oldRevision As Variant
    Dim oldQuantity As Variant

    Dim newLevel As Variant
    Dim newRevision As Variant
    Dim newQuantity As Variant

    Dim quantityDiff As Variant


    oldLevel = Empty
    oldRevision = Empty
    oldQuantity = Empty

    newLevel = Empty
    newRevision = Empty
    newQuantity = Empty

    quantityDiff = Empty


    '===========================================================================
    ' 旧BOM
    '===========================================================================
    If IsArray(oldRow) Then

        oldLevel = oldRow(0)
        oldRevision = oldRow(1)
        oldQuantity = oldRow(2)

    End If


    '===========================================================================
    ' 新BOM
    '===========================================================================
    If IsArray(newRow) Then

        newLevel = newRow(0)
        newRevision = newRow(1)
        newQuantity = newRow(2)

    End If


    '===========================================================================
    ' 数量差 = 新数量 - 旧数量
    '===========================================================================
    If IsArray(oldRow) _
        And IsArray(newRow) Then

        If Not IsEmpty(oldQuantity) _
            And Not IsEmpty(newQuantity) Then

            quantityDiff = _
                CDbl(newQuantity) - _
                CDbl(oldQuantity)

        End If

    End If


    result.Add _
        Array( _
            diffType, _
            oldLevel, _
            oldRevision, _
            oldQuantity, _
            newLevel, _
            newRevision, _
            newQuantity, _
            quantityDiff)

End Sub


'===============================================================================
' BOM比較キー
'
' レベル + リビジョン名
'
' 数量は含めない。
' 数量までキーにすると数量変更が「削除 + 追加」になるため。
'===============================================================================
Private Function BOMKey( _
    rowData As Variant) As String

    BOMKey = _
        VariantToText(rowData(0)) & _
        "|" & _
        CStr(rowData(1))

End Function


'===============================================================================
' 同じレベルか判定
'===============================================================================
Private Function SameLevel( _
    oldRow As Variant, _
    newRow As Variant) As Boolean

    If IsEmpty(oldRow(0)) _
        Or IsEmpty(newRow(0)) Then

        SameLevel = False

    Else

        SameLevel = _
            CLng(oldRow(0)) = _
            CLng(newRow(0))

    End If

End Function


'===============================================================================
' Variant → 文字列
'===============================================================================
Private Function VariantToText( _
    v As Variant) As String

    If IsEmpty(v) _
        Or IsNull(v) Then

        VariantToText = ""

    Else

        VariantToText = CStr(v)

    End If

End Function


'===============================================================================
' 数量比較
'===============================================================================
Private Function QuantityEqual( _
    a As Variant, _
    b As Variant) As Boolean

    Const TOLERANCE As Double = _
        0.000000001

    If IsEmpty(a) _
        And IsEmpty(b) Then

        QuantityEqual = True

        Exit Function

    End If


    If IsEmpty(a) _
        Or IsEmpty(b) Then

        QuantityEqual = False

        Exit Function

    End If


    QuantityEqual = _
        Abs( _
            CDbl(a) - _
            CDbl(b)) _
        <= TOLERANCE

End Function


'===============================================================================
' 差分シートを準備
'===============================================================================
Private Function PrepareResultSheet() As Worksheet

    Dim ws As Worksheet

    On Error Resume Next

    Set ws = _
        ThisWorkbook.Worksheets( _
            "差分")

    On Error GoTo 0


    '===========================================================================
    ' なければ作成
    '===========================================================================
    If ws Is Nothing Then

        Set ws = _
            ThisWorkbook.Worksheets.Add( _
                After:= _
                ThisWorkbook.Worksheets( _
                    ThisWorkbook.Worksheets.Count))

        ws.Name = "差分"

    Else

        '=======================================================================
        ' 前回結果を完全クリア
        '=======================================================================
        ws.Cells.Clear

    End If


    Set PrepareResultSheet = ws

End Function


'===============================================================================
' 結果表示
'
' Collectionを直接1行ずつExcelへ書かず、
' 一度2次元配列に変換して一括出力する。
'===============================================================================
Private Sub WriteResults( _
    ws As Worksheet, _
    diffData As Collection)

    Dim headers(1 To 1, 1 To 8) As Variant

    Dim outputData() As Variant

    Dim i As Long
    Dim j As Long

    Dim rowData As Variant


    '===========================================================================
    ' ヘッダー
    '===========================================================================
    headers(1, 1) = "区分"
    headers(1, 2) = "旧レベル"
    headers(1, 3) = "旧リビジョン名"
    headers(1, 4) = "旧数量"

    headers(1, 5) = "新レベル"
    headers(1, 6) = "新リビジョン名"
    headers(1, 7) = "新数量"

    headers(1, 8) = "数量差"


    ws.Range( _
        "A1:H1").Value = headers


    '===========================================================================
    ' 差分なし
    '===========================================================================
    If diffData.Count = 0 Then

        ws.Range( _
            "A2").Value = _
            "差分はありません。"

        Exit Sub

    End If


    '===========================================================================
    ' 結果用2次元配列
    '===========================================================================
    ReDim outputData( _
        1 To diffData.Count, _
        1 To 8)


    '===========================================================================
    ' Collection → 配列
    '===========================================================================
    For i = 1 To diffData.Count

        rowData = diffData(i)

        For j = 1 To 8

            If Not IsEmpty( _
                rowData(j - 1)) Then

                outputData(i, j) = _
                    rowData(j - 1)

            Else

                outputData(i, j) = ""

            End If

        Next j

    Next i


    '===========================================================================
    ' Excelへ一括出力
    '===========================================================================
    ws.Range( _
        "A2").Resize( _
            diffData.Count, _
            8).Value = _
        outputData

End Sub


'===============================================================================
' 結果シート書式設定
'===============================================================================
Private Sub FormatResultSheet( _
    ws As Worksheet)

    Dim lastRow As Long

    Dim r As Long
    Dim diffType As String


    lastRow = _
        ws.Cells( _
            ws.Rows.Count, _
            "A").End(xlUp).Row


    '===========================================================================
    ' ヘッダー
    '===========================================================================
    With ws.Range( _
        "A1:H1")

        .Font.Bold = True

        .HorizontalAlignment = _
            xlCenter

        .VerticalAlignment = _
            xlCenter

        .Interior.Color = _
            RGB(217, 225, 242)

    End With


    '===========================================================================
    ' 数量表示
    '===========================================================================
    ws.Columns("D").NumberFormat = _
        "0.######"

    ws.Columns("G").NumberFormat = _
        "0.######"


    '===========================================================================
    ' 数量差
    '===========================================================================
    ws.Columns("H").NumberFormat = _
        "+0.######;-0.######;0"


    '===========================================================================
    ' 差分種別ごとの色
    '===========================================================================
    If lastRow >= 2 Then

        For r = 2 To lastRow

            diffType = _
                CStr( _
                    ws.Cells(r, 1).Value)

            Select Case diffType

                Case "追加"

                    ws.Range( _
                        "A" & r & _
                        ":H" & r).Interior.Color = _
                        RGB(226, 239, 218)

                Case "削除"

                    ws.Range( _
                        "A" & r & _
                        ":H" & r).Interior.Color = _
                        RGB(255, 199, 206)

                Case "置換"

                    ws.Range( _
                        "A" & r & _
                        ":H" & r).Interior.Color = _
                        RGB(255, 235, 156)

                Case "数量変更"

                    ws.Range( _
                        "A" & r & _
                        ":H" & r).Interior.Color = _
                        RGB(221, 235, 247)

            End Select

        Next r

    End If


    '===========================================================================
    ' 罫線
    '===========================================================================
    With ws.Range( _
        "A1:H" & lastRow).Borders

        .LineStyle = xlContinuous
        .Weight = xlThin

    End With


    '===========================================================================
    ' 列幅
    '===========================================================================
    ws.Columns("A:H").AutoFit

    If ws.Columns("A").ColumnWidth < 10 Then
        ws.Columns("A").ColumnWidth = 10
    End If

    If ws.Columns("C").ColumnWidth < 22 Then
        ws.Columns("C").ColumnWidth = 22
    End If

    If ws.Columns("F").ColumnWidth < 22 Then
        ws.Columns("F").ColumnWidth = 22
    End If


    '===========================================================================
    ' レベル中央寄せ
    '===========================================================================
    ws.Columns("B").HorizontalAlignment = _
        xlCenter

    ws.Columns("E").HorizontalAlignment = _
        xlCenter


    '===========================================================================
    ' フィルター
    '===========================================================================
    If lastRow >= 1 Then

        ws.Range( _
            "A1:H" & lastRow).AutoFilter

    End If


    '===========================================================================
    ' ウィンドウ固定
    '===========================================================================
    ws.Activate

    ActiveWindow.FreezePanes = False

    ActiveWindow.SplitRow = 1
    ActiveWindow.SplitColumn = 0

    ActiveWindow.FreezePanes = True


    ws.Range("A1").Select

End Sub


'===============================================================================
' 比較結果を新しいExcelファイルとして保存
'
' 保存先:
'   新BOMと同じフォルダ
'
' ファイル名:
'   BOM比較_旧ファイル名_to_新ファイル名.xlsx
'
' 例:
'   BOM比較_MF2299_to_MF2300.xlsx
'
' 同名ファイルが存在する場合:
'   BOM比較_MF2299_to_MF2300_20260929_133500.xlsx
'===============================================================================
Private Function ExportComparisonResult( _
    resultSheet As Worksheet, _
    oldFile As String, _
    newFile As String) As String

    Dim outputFolder As String
    Dim outputFileName As String
    Dim outputPath As String

    Dim oldName As String
    Dim newName As String

    Dim wbOut As Workbook
    Dim wsOut As Worksheet

    Dim fileSystem As Object

    Dim r As Long

    Dim savedErrNumber As Long
    Dim savedErrDescription As String


    On Error GoTo ErrorHandler


    '===========================================================================
    ' ファイル名から拡張子を除く
    '===========================================================================
    oldName = GetFileBaseName(oldFile)
    newName = GetFileBaseName(newFile)


    '===========================================================================
    ' ファイル名に使えない文字を除去
    '===========================================================================
    oldName = SanitizeFileName(oldName)
    newName = SanitizeFileName(newName)


    '===========================================================================
    ' 保存先 = 新BOMと同じフォルダ
    '===========================================================================
    outputFolder = _
        Left$( _
            newFile, _
            InStrRev( _
                newFile, _
                Application.PathSeparator))


    '===========================================================================
    ' 出力ファイル名
    '===========================================================================
    outputFileName = _
        "BOM比較_" & _
        oldName & _
        "_to_" & _
        newName & _
        ".xlsx"


    outputPath = _
        outputFolder & _
        outputFileName


    '===========================================================================
    ' 同名ファイル確認
    '===========================================================================
    Set fileSystem = _
        CreateObject( _
            "Scripting.FileSystemObject")


    If fileSystem.FileExists( _
        outputPath) Then

        outputFileName = _
            "BOM比較_" & _
            oldName & _
            "_to_" & _
            newName & _
            "_" & _
            Format$( _
                Now, _
                "yyyymmdd_hhnnss") & _
            ".xlsx"


        outputPath = _
            outputFolder & _
            outputFileName

    End If


    '===========================================================================
    ' 新しいブックを作成
    '===========================================================================
    Set wbOut = _
        Workbooks.Add( _
            xlWBATWorksheet)


    Set wsOut = _
        wbOut.Worksheets(1)


    wsOut.Name = "差分"


    '===========================================================================
    ' 比較結果をコピー
    '===========================================================================
    resultSheet.UsedRange.Copy


    With wsOut.Range("A1")

        .PasteSpecial _
            Paste:=xlPasteAll

        .PasteSpecial _
            Paste:=xlPasteColumnWidths

    End With


    Application.CutCopyMode = False


    '===========================================================================
    ' 行の高さをコピー
    '===========================================================================
    For r = 1 To _
        resultSheet.UsedRange.Rows.Count

        wsOut.Rows(r).RowHeight = _
            resultSheet.Rows(r).RowHeight

    Next r


    '===========================================================================
    ' 先頭行固定
    '===========================================================================
    wbOut.Activate
    wsOut.Activate

    ActiveWindow.FreezePanes = False

    ActiveWindow.SplitRow = 1
    ActiveWindow.SplitColumn = 0

    ActiveWindow.FreezePanes = True


    wsOut.Range("A1").Select


    '===========================================================================
    ' xlsxとして保存
    '===========================================================================
    wbOut.SaveAs _
        Filename:=outputPath, _
        FileFormat:=xlOpenXMLWorkbook


    '===========================================================================
    ' 出力ブックを閉じる
    '===========================================================================
    wbOut.Close _
        SaveChanges:=False


    Set wbOut = Nothing
    Set wsOut = Nothing


    ExportComparisonResult = _
        outputPath

    Exit Function


ErrorHandler:

    savedErrNumber = Err.Number
    savedErrDescription = Err.Description

    On Error Resume Next

    Application.CutCopyMode = False

    If Not wbOut Is Nothing Then

        wbOut.Close _
            SaveChanges:=False

    End If

    On Error GoTo 0

    Err.Raise _
        savedErrNumber, _
        "ExportComparisonResult", _
        savedErrDescription

End Function


'===============================================================================
' フルパスから拡張子を除いたファイル名を取得
'
' C:\ABC\MF2299.xlsm
' ↓
' MF2299
'===============================================================================
Private Function GetFileBaseName( _
    filePath As String) As String

    Dim fileName As String
    Dim dotPosition As Long


    '===========================================================================
    ' フォルダ部分を除去
    '===========================================================================
    fileName = _
        Mid$( _
            filePath, _
            InStrRev( _
                filePath, _
                Application.PathSeparator) + 1)


    '===========================================================================
    ' 拡張子を除去
    '===========================================================================
    dotPosition = _
        InStrRev( _
            fileName, _
            ".")


    If dotPosition > 1 Then

        fileName = _
            Left$( _
                fileName, _
                dotPosition - 1)

    End If


    GetFileBaseName = _
        fileName

End Function


'===============================================================================
' Windowsでファイル名に使用できない文字を "_" に置換
'
' \ / : * ? " < > |
'===============================================================================
Private Function SanitizeFileName( _
    fileName As String) As String

    Dim invalidChars As Variant
    Dim c As Variant


    invalidChars = _
        Array( _
            "\", _
            "/", _
            ":", _
            "*", _
            "?", _
            """", _
            "<", _
            ">", _
            "|")


    For Each c In invalidChars

        fileName = _
            Replace( _
                fileName, _
                CStr(c), _
                "_")

    Next c


    SanitizeFileName = _
        fileName

End Function
