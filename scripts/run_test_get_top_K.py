import sys
sys.path.insert(0, r'c:/Users/maor livni/PycharmProjects/IR_Project')
import tests.test_get_top_K as t

if __name__ == '__main__':
    try:
        t.main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise
