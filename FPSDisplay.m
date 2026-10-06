#import <UIKit/UIKit.h>
static UILabel *fpsLabel;
static NSInteger fpsCount;
static NSTimeInterval lastTime;
static CADisplayLink *displayLink;

%hook UIWindow
- (void)layoutSubviews {
    %orig;
    if (!fpsLabel) {
        fpsLabel = [[UILabel alloc] initWithFrame:CGRectMake(15, 45, 250, 20)];
        fpsLabel.text = @"ThanhHung FPS";
        fpsLabel.textColor = [UIColor greenColor];
        fpsLabel.backgroundColor = [UIColor clearColor];
        fpsLabel.font = [UIFont boldSystemFontOfSize:13];
        [self addSubview:fpsLabel];
    }
}
%new
- (void)updateFPS:(CADisplayLink *)link {
    fpsCount++;
    NSTimeInterval now = link.timestamp;
    if (now - lastTime >= 1.0) {
        fpsLabel.text = [NSString stringWithFormat:@"ThanhHung - %ld FPS", (long)fpsCount];
        fpsCount = 0;
        lastTime = now;
    }
}
%end
