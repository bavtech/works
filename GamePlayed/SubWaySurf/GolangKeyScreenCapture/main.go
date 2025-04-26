package main

import (
	"fmt"
	"image/png"
	"log"
	"os"
	"time"

	"github.com/eiannone/keyboard"
	"github.com/kbinani/screenshot"
	hook "github.com/robotn/gohook"
)

func captureScreen(fileName string) error {
	n := screenshot.NumActiveDisplays()
	if n <= 0 {
		return fmt.Errorf("no active displays")
	}
	bounds := screenshot.GetDisplayBounds(0)

	img, err := screenshot.CaptureRect(bounds)
	if err != nil {
		return err
	}

	file, err := os.Create(fileName)
	if err != nil {
		return err
	}
	defer file.Close()

	return png.Encode(file, img)
}

func globalListenKeys(evChan chan hook.Event) {

	for ev := range evChan {

		switch ev.Keychar {
		case 'a':

			go captureScreen("left_.png")
		case 's':
			go captureScreen("down_.png")

		case 'd':
			go captureScreen("right_.png")
		case 'w':
			go captureScreen("jump_.png")
		}

		if ev.Keycode == 1 { // ESC key
			break
		}
	}
}
func listenKeys() {
	if err := keyboard.Open(); err != nil {
		log.Fatal(err)
	}
	defer keyboard.Close()

	for {
		char, key, err := keyboard.GetKey()
		if err != nil {
			log.Fatal(err)
		}

		switch char {
		case 'a':

			go captureScreen("left_.png")
		case 's':
			go captureScreen("down_.png")

		case 'd':
			go captureScreen("right_.png")
		case 'w':
			go captureScreen("jump_.png")
		}

		if char == 'a' {
		}
		fmt.Printf("Pressed: rune=%q, key=%v\n", char, key)

		// You can now call captureScreen here with a timestamped or labeled filename
	}
}

func main() {
	evChan := hook.Start()
	defer hook.End()

	// captureScreen("something.png")
	// globalListenKeys(evChan)

	timestamp := time.Now().Format("20060102_150405")
	// what does this do

	fmt.Println(timestamp)
}
