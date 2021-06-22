// Will contain the following variables: imageURLs, descriptions, titles and articleURLs
$variables

// Counter for knowing which article has been reached when pressing the left or right arrow
currentCounter = 0

// Previewnumber is determining which of the preview windows is changed (0 for the left, 1 for the on in the middle and 2 for the right) and detailNumber is determining which entry in the arrays storing the title, sourceurls, imageurls and descriptions is used
function changeIndividualPreview(previewNumber, detailNumber){


	document.querySelectorAll('a.article-link')[previewNumber].setAttribute("href", articleURLs[detailNumber])
	document.querySelectorAll('img.article-image')[previewNumber].setAttribute("src", imageURLs[detailNumber])
	document.querySelectorAll('div.desc h2')[previewNumber].textContent = titles[detailNumber]
	document.querySelectorAll('div.desc p')[previewNumber].textContent = descriptions[detailNumber]

}

// The currentNumber is variable for telling how far the user has scrolled right or left using the arrows (will often just be currentCounter)
function changePreviews(currentNumber){
	for (let i = 0; i < 3; i++){
		changeIndividualPreview(i, ((i + currentNumber) % (imageURLs.length - 1)))
	}
}

function arrowPress(left) {
	if (left == true) {
		currentCounter = currentCounter - 3

		if (currentCounter < 0) {
			currentCounter = (imageURLs.length - 1) + currentCounter
		}

		changePreviews(currentCounter)

	} else {

		currentCounter = (currentCounter + 3) % (imageURLs.length - 1)
		changePreviews(currentCounter)

	}
}

document.addEventListener('keydown', (event) => {
	if (event.code == "ArrowLeft") arrowPress(true);
	else if (event.code == "ArrowRight") arrowPress(false);
});
