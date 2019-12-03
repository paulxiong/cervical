package util

//RemoveDuplicatesAndEmpty 字符串数组去重,去空
func RemoveDuplicatesAndEmpty(strSlice []string) []string {
	var strMap = make(map[string]string)
	for _, v := range strSlice {
		if v == "" {
			continue
		}
		strMap[v] = v
	}

	var secondStr []string
	for _, value := range strMap {
		secondStr = append(secondStr, value)
	}
	return secondStr
}
