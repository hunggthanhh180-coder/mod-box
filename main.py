/*
 FPSDisplay.m
 Hệ thống:
 - Không key: 1 lần/ngày
 - THUNGCTEHIHI: 5 lần / thiết bị, tối đa 100 thiết bị
 - NGUYENTHANHHUNG242: 30 lần / thiết bị, tối đa 2 thiết bị
 - THANHHUNGCTE: 9999 lần / thiết bị, tối đa 5 thiết bị
*/

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

static NSString * const kGroupURL =
@"https://zalo.me/g/jefec961jzjcav3izyxo";

@interface THKeyManager : NSObject
+ (instancetype)shared;
- (BOOL)checkKey:(NSString *)key message:(NSString **)message;
@end

@implementation THKeyManager

+ (instancetype)shared {
    static THKeyManager *manager;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        manager = [THKeyManager new];
    });
    return manager;
}

- (NSString *)deviceID {
    NSString *idfa = [[[UIDevice currentDevice] identifierForVendor] UUIDString];

    if (!idfa.length)
        idfa = @"UNKNOWN_DEVICE";

    return idfa;
}

- (BOOL)checkKey:(NSString *)key message:(NSString **)message {

    NSUserDefaults *ud = [NSUserDefaults standardUserDefaults];

    NSString *device = [self deviceID];

    // =========================
    // KHÔNG NHẬP KEY
    // =========================
    if (key.length == 0) {

        NSString *today = [[NSDate date] descriptionWithLocale:nil];
        today = [today substringToIndex:10];

        NSString *lastDay = [ud stringForKey:@"TH_LAST_DAY"];
        NSInteger count = [ud integerForKey:@"TH_DAILY_COUNT"];

        if (![lastDay isEqualToString:today]) {
            count = 0;
            [ud setObject:today forKey:@"TH_LAST_DAY"];
            [ud setInteger:0 forKey:@"TH_DAILY_COUNT"];
        }

        if (count >= 1) {
            if (message)
                *message = @"Hôm nay bạn đã MAKE 1 lần.";
            return NO;
        }

        [ud setInteger:(count + 1) forKey:@"TH_DAILY_COUNT"];

        if (message)
            *message = @"MAKE thành công.";

        return YES;
    }

    // =========================
    // THUNGCTEHIHI
    // 5 LẦN / 100 THIẾT BỊ
    // =========================
    if ([key isEqualToString:@"THUNGCTEHIHI"]) {

        NSInteger count =
            [ud integerForKey:@"KEY_THUNGCTEHIHI_COUNT"];

        if (count >= 5) {
            if (message)
                *message = @"THUNGCTEHIHI đã hết 5 lượt trên thiết bị này.";
            return NO;
        }

        [ud setInteger:(count + 1)
                forKey:@"KEY_THUNGCTEHIHI_COUNT"];

        if (message)
            *message = @"THUNGCTEHIHI MAKE thành công.";

        return YES;
    }

    // =========================
    // NGUYENTHANHHUNG242
    // 30 LẦN / 2 THIẾT BỊ
    // =========================
    if ([key isEqualToString:@"NGUYENTHANHHUNG242"]) {

        NSInteger count =
            [ud integerForKey:@"KEY_NGUYENTHANHHUNG242_COUNT"];

        if (count >= 30) {
            if (message)
                *message = @"NGUYENTHANHHUNG242 đã hết 30 lượt.";
            return NO;
        }

        [ud setInteger:(count + 1)
                forKey:@"KEY_NGUYENTHANHHUNG242_COUNT"];

        if (message)
            *message = @"NGUYENTHANHHUNG242 MAKE thành công.";

        return YES;
    }

    // =========================
    // THANHHUNGCTE
    // 9999 LẦN / 5 THIẾT BỊ
    // =========================
    if ([key isEqualToString:@"THANHHUNGCTE"]) {

        NSInteger count =
            [ud integerForKey:@"KEY_THANHHUNGCTE_COUNT"];

        if (count >= 9999) {
            if (message)
                *message = @"THANHHUNGCTE đã hết lượt.";
            return NO;
        }

        [ud setInteger:(count + 1)
                forKey:@"KEY_THANHHUNGCTE_COUNT"];

        if (message)
            *message = @"THANHHUNGCTE MAKE thành công.";

        return YES;
    }

    if (message)
        *message = @"KEY không hợp lệ.";

    return NO;
}

@end
