import pytest
import testerapp.testerapp 

input_data_0 = ['\n']
input_data_1 = ['000101020001ff02\n']
input_data_2 = ['00000101FF\n']
input_data_3 = ['0021X455\n']

result_0 = 'FFFFEEEE'
result_1 = '0003FFFFFF00FFFF0000'
result_2 = '0001FFFFEEEE'
result_3 = 'FFFFFFFF'


@pytest.mark.parametrize(
    "input_data, result, exc",
    [ [input_data_0, result_0, None],
      [input_data_1, result_1, None],
      [input_data_2, result_2, None],
      [input_data_3, result_3, ValueError],
    ]
)
def test_main(monkeypatch, input_data, result, exc):
    def mock_file_writer(filen, mode, output):
        print(output)
    def mock_file_read(filen, mode):
        return input_data
    mock_sys = ['main', 'TestInput00.txt']

    monkeypatch.setattr('testerapp.testerapp.file_writer', mock_file_writer)
    monkeypatch.setattr('testerapp.testerapp.file_read', mock_file_read)
    monkeypatch.setattr('testerapp.testerapp.sys.argv', mock_sys)
    if exc:
        with pytest.raises(exc):
            testerapp.testerapp.main()
    else:
        assert result == testerapp.testerapp.main()
        



