package main

import (
	"fmt"
	"image"
	"image/png"
	"log"
	"os"
	"strings"
	"time"

	"github.com/kbinani/screenshot"
	hook "github.com/robotn/gohook"
)

var (
	THRESHOLD         = 6000
	noActionThreshold = 20000
	startIntake       = false
	folderPath        = "./Actions"
)

func captureScreen(fileName string) error {
	n := screenshot.NumActiveDisplays()
	if n <= 0 {
		return fmt.Errorf("no active displays")
	}
	bounds := screenshot.GetDisplayBounds(0)
	halfWidth := (bounds.Max.X - bounds.Min.X) / 2

	// this will capture half of the width and full height
	captureRect := image.Rect(
		bounds.Min.X+halfWidth, // left
		bounds.Min.Y,           // top
		bounds.Max.X,           // right (half screen)
		bounds.Max.Y,           // bottom (full height)
	)

	img, err := screenshot.CaptureRect(captureRect)
	if err != nil {
		return err
	}

	timestamp := time.Now().Format("20060102_150405")
	fileName = fmt.Sprintf("%s/%s_%s.png", folderPath, fileName, timestamp)

	file, err := os.Create(fileName)
	if err != nil {
		return err
	}
	defer file.Close()

	return png.Encode(file, img)
}

func globalListenKeys(evChan chan hook.Event) {

	right := countImagesWithPrefix(folderPath, "right")
	left := countImagesWithPrefix(folderPath, "left")
	jump := countImagesWithPrefix(folderPath, "jump")
	roll := countImagesWithPrefix(folderPath, "roll")
	noAction := countImagesWithPrefix(folderPath, "noAction")
	p1 := false
	p2 := false
	for ev := range evChan {

		switch ev.Keychar {
		case 'a':

			if left <= THRESHOLD {

				captureScreen("left")
				left++
			}

		case 's':

			if roll <= THRESHOLD {
				captureScreen("down")
				roll++
			}

		case 'd':
			if right <= THRESHOLD {
				captureScreen("right")
				right++
			}

		case 'w':
			if jump <= THRESHOLD {
				captureScreen("jump")
				jump++
			}
		case '+':
			startIntakeSwitch()
		}

		if startIntake {
			if p2 {

				fmt.Println("capturing input")
			}
			if noAction <= noActionThreshold {
				captureScreen("noAction")
				noAction++
				time.Sleep(100 * time.Millisecond)
				p1 = !p1

			}
		} else {
			if p1 {

				fmt.Println("Capturing paused")
				p2 = !p2

			}

		}
		if ev.Keycode == 1 { // ESC key
			os.Exit(0)
		}
	}

}

func countImagesWithPrefix(folderPath string, prefix string) int {
	files, err := os.ReadDir(folderPath)
	if err != nil {
		log.Fatal(err)
	}

	count := 0
	for _, file := range files {
		if !file.IsDir() && strings.HasPrefix(file.Name(), prefix) && strings.HasSuffix(file.Name(), ".png") {
			count++
		}
	}
	return count
}
func startIntakeSwitch() {
	startIntake = !startIntake
}
func main() {

	// start Hook Channel
	evChan := hook.Start()
	defer hook.End()

	// captureScreen("something")

	globalListenKeys(evChan)

	// timestamp := time.Now().Format("20060102_150405")
	// // what does this do

	// fmt.Println(timestamp)

}
