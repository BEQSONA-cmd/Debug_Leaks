#include <cstdlib>
#include <fstream>
#include <iostream>

void	ft_putstr_fd(const char *s, std::ostream &os)
{
	os << s;
}

int	main(void)
{
	const char	*home = getenv("HOME");
	char		path[1024];

	if (home == nullptr)
	{
		std::cerr << "Error getting home directory" << std::endl;
		return (1);
	}
	snprintf(path, sizeof(path), "%s/.zshrc", home);
	std::ofstream file(path, std::ios::out | std::ios::app);
	if (!file.is_open())
	{
		perror("Error opening the file");
		return (1);
	}
	else
	{
		ft_putstr_fd("\n", file);
		ft_putstr_fd("alias dl='python3 ~/Debug_Leaks/leaks.py'\n", file);
	}
	file.close();
	return (0);
}
