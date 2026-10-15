#import <UIKit/UIKit.h>

@interface FPSDisplay : NSObject
+ (instancetype)sharedInstance;
- (void)show;
- (void)hide;
@end
#import "FPSDisplay.h"
#import <QuartzCore/QuartzCore.h>

@interface FPSDisplay () {
    UIWindow *_window;
    UILabel *_label;
    CADisplayLink *_displayLink;
    NSTimeInterval _lastTime;
    NSUInteger _count;
}
@end

@implementation FPSDisplay

+ (instancetype)sharedInstance {
    static FPSDisplay *sharedInstance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedInstance = [[self alloc] init];
    });
    return sharedInstance;
}

- (instancetype)init {
    self = [super init];
    if (self) {
        _window = [[UIWindow alloc] initWithFrame:CGRectMake(20, 40, 85, 26)];
        _window.windowLevel = UIWindowLevelAlert + 9999;
        _window.backgroundColor = [UIColor colorWithWhite:0.0 alpha:0.7];
        _window.layer.cornerRadius = 6;
        _window.clipsToBounds = YES;
        
        _label = [[UILabel alloc] initWithFrame:_window.bounds];
        _label.textAlignment = NSTextAlignmentCenter;
        _label.textColor = [UIColor greenColor];
        _label.font = [UIFont boldSystemFontOfSize:13];
        _label.text = @"FPS: --";
        [_window addSubview:_label];
        
        [self show];
    }
    return self;
}

- (void)show {
    _window.hidden = NO;
    if (!_displayLink) {
        _displayLink = [CADisplayLink displayLinkWithTarget:self selector:@selector(tick:)];
        [_displayLink addToRunLoop:[NSRunLoop mainRunLoop] forMode:NSRunLoopCommonModes];
    }
}

- (void)hide {
    _window.hidden = YES;
    [_displayLink invalidate];
    _displayLink = nil;
}

- (void)tick:(CADisplayLink *)link {
    if (_lastTime == 0) {
        _lastTime = link.timestamp;
        return;
    }
    
    _count++;
    NSTimeInterval delta = link.timestamp - _lastTime;
    if (delta >= 1.0) {
        NSInteger fps = (NSInteger)(_count / delta);
        _label.text = [NSString stringWithFormat:@"FPS: %ld", (long)fps];
        
        if (fps >= 50) {
            _label.textColor = [UIColor greenColor];
        } else if (fps >= 30) {
            _label.textColor = [UIColor yellowColor];
        } else {
            _label.textColor = [UIColor redColor];
        }
        
        _lastTime = link.timestamp;
        _count = 0;
    }
}

@end
TARGET = iphone:clang:latest:14.0
ARCHS = arm64 arm64e

include $(THEOS)/makefiles/common.mk

TWEAK_NAME = NguyenThanhHung

NguyenThanhHung_FILES = FPSDisplay.m
ThanhHungCte_FRAMEWORKS = UIKit QuartzCore

include $(THEOS_MAKE_PATH)/tweak.mk
Package: com.thanhhung.fpsdisplay
Name: FPS Display Tweak
Depends: mobilesubstrate
Version: 1.0.0
Architecture: iphoneos-arm
Description: Tweak hiển thị FPS màn hình mượt mà.
Maintainer: ThanhHung
Author: Hungg
{
    Filter = {
        Bundles = (
            "com.apple.springboard",
        );
    };
}

Section: Tweaks
#!/bin/bash
echo "Đang tiến hành build tweak..."
make package
echo "Hoàn tất!"
import os
import subprocess

def main():
    print("Bắt đầu build project tự động bằng Python...")
    result = subprocess.run(["make", "package"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode == 0:
        print("Build thành công!")
    else:
        print("Build thất bại:", result.stderr)

if __name__ == "__main__":
    main()
requests>=2.28.0
