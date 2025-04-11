export default function getStadeColor(stade: number) {
	switch (stade) {
		case 1:
			return 'success'
		case 2:
			return 'info'
		case 3:
			return 'neutral'
		case 4:
			return 'warning'
		case 5:
			return 'error'
		default:
			return 'success'
	}
}